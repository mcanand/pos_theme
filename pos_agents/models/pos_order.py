from odoo import fields, models, api, _
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = 'pos.order'

    agent_id = fields.Many2one('res.partner', domain=[('agent_rank', '>', 0)])
    agent_invoice_ids = fields.One2many('account.move', 'pos_order_id')
    agent_invoice_ids_count = fields.Integer(compute="_compute_agent_invoice_count")

    @api.depends('agent_invoice_ids', 'partner_id', 'agent_id')
    def _compute_agent_invoice_count(self):
        for rec in self:
            rec.agent_invoice_ids_count = len(rec.agent_invoice_ids)

    def _generate_pos_order_invoice(self):
        res = super(PosOrder, self)._generate_pos_order_invoice()
        for order in self:
            order.create_agent_bill()
        return res

    def _get_fields_for_draft_order(self):
        res_fields = super(PosOrder, self)._get_fields_for_draft_order()
        res_fields.extend(['agent_id'])
        return res_fields

    def _export_for_ui(self, order):
        res = super(PosOrder, self)._export_for_ui(order)
        res['agent_id'] = order.agent_id.id
        return res

    @api.model
    def _order_fields(self, ui_order):
        order_fields = super(PosOrder, self)._order_fields(ui_order)
        order_fields['agent_id'] = ui_order.get('agent_id')
        return order_fields

    def get_agent_commission(self):
        commission = self.agent_id.agent_comm
        total = self.amount_total
        amount = (commission / 100) * total
        return amount

    def prepare_agent_invoice_lines(self):
        name = self.agent_id.product_id.get_product_multiline_description_sale()
        return (0, 0, {
            'product_id': self.agent_id.product_id.id,
            'quantity': 1,
            'discount': 0,
            'account_id':
                self.agent_id.product_id.product_tmpl_id.with_company(self.company_id)._get_product_accounts()[
                    'expense'].id,
            'price_unit': self.get_agent_commission(),
            'name': name,
            'tax_ids': []
        })

    def create_agent_bill(self):
        if self.agent_id and not self.agent_invoice_ids:
            vals = self._prepare_invoice_vals()
            vals['partner_id'] = self.agent_id.id
            vals['pos_order_id'] = self.id
            vals['move_type'] = 'in_invoice'
            vals['journal_id'] = self.agent_id.journal_id.id
            vals['invoice_line_ids'] = [self.prepare_agent_invoice_lines()]
            bill = self.env['account.move'].create(vals)
            bill.sudo().with_company(self.company_id)._post()
            return bill
        return False

    def action_view_agent_invoice(self):
        if not self.agent_invoice_ids.ids:
            raise ValidationError(_('There is no agent bill for this pos order'))
        return {
            'name': _('Agent Invoice'),
            'view_mode': 'form',
            'view_id': self.env.ref('account.view_move_form').id,
            'res_model': 'account.move',
            'context': "{'move_type':'in_invoice'}",
            'type': 'ir.actions.act_window',
            'res_id': self.agent_invoice_ids.ids[0],
        }


class AccountMove(models.Model):
    _inherit = 'account.move'

    pos_order_id = fields.Many2one('pos.order')
