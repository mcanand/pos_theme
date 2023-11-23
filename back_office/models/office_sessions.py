from odoo import fields, models, api, _
from datetime import datetime
from odoo.exceptions import ValidationError


class OfficeSession(models.Model):
    _name = "office.session"

    name = fields.Char(default=lambda self: _('New'))
    sale_id = fields.Many2one('office.sale')
    user_id = fields.Many2one('res.users', string="Responsible", default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.company)
    start_at = fields.Datetime(string="Start at")
    end_at = fields.Datetime(string="Ended at")
    state = fields.Selection([('in_progress', 'In Progress'), ('closed', 'Closed & Posted')], default='in_progress')
    order_ids = fields.One2many('office.order', 'session_id')
    order_count = fields.Integer(compute="_compute_order_count")

    @api.depends('order_ids')
    def _compute_order_count(self):
        for rec in self:
            rec.order_count = len(rec.order_ids)

    def action_continue(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'office.order',
            'view_mode': 'form',
            'target': 'current',
            'view_id': self.env.ref('back_office.view_office_order_form').id,
            'views': [(False, 'form')],
            'context': {'default_session_id': self.id}
        }

    def action_close(self):
        orders = [x for x in self.order_ids if x.state in ['draft', 'hold']]
        if orders:
            raise ValidationError(_("Some Orders Are still in draft state delete or complete the order"))
        orders_to_invoice = [x for x in self.order_ids if x.state in ['confirm']]
        if orders_to_invoice:
            for order in orders_to_invoice:
                order._create_invoice()
        self.end_at = datetime.now()
        self.state = 'closed'

    def action_view_orders(self):
        if self.order_ids:
            return {
                'name': 'Orders',
                'type': 'ir.actions.act_window',
                'res_model': 'office.order',
                'view_mode': 'tree,form',
                "context": {"create": False, },
                "domain": [('id', 'in', self.order_ids.ids)],
                'views': [[False, "tree"], [False, "form"]],
            }

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'office.session') or _('New')
        res = super(OfficeSession, self).create(vals)
        return res
