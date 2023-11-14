from collections import defaultdict

from odoo import fields, models, api, _
import json
from odoo.tools.misc import get_lang
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_code = fields.Char(string="Customer Code")


class OfficeOrder(models.Model):
    _name = "office.order"
    _description = 'Back Office Orders'
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin', 'utm.mixin']

    name = fields.Char(
        string="Order Reference",
        required=True, copy=False, readonly=True,
        index='trigram',
        states={'draft': [('readonly', False)]},
        default=lambda self: _('New'))

    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string="Customer",
        required=True, readonly=False, change_default=True, index=True,
        tracking=1,
        domain="[('type', '!=', 'private'), ('company_id', 'in', (False, company_id))]")
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('confirm', "Confirm"),
        ],
        string="Status",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='draft')

    company_id = fields.Many2one(
        comodel_name='res.company',
        required=True, index=True,
        default=lambda self: self.env.company)

    date_order = fields.Datetime(
        string="Order Date",
        required=True, readonly=False, copy=False,
        help="Creation date of draft/sent orders,\nConfirmation date of confirmed orders.",
        default=fields.Datetime.now)
    customer_code = fields.Char(string="Customer Code", related='partner_id.customer_code')
    partner_invoice_id = fields.Many2one(
        comodel_name='res.partner',
        string="Invoice Address",
        compute='_compute_partner_invoice_id',
        store=True, readonly=False, required=True, precompute=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")

    partner_shipping_id = fields.Many2one(
        comodel_name='res.partner',
        string="Delivery Address",
        compute='_compute_partner_shipping_id',
        store=True, readonly=False, required=True, precompute=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]", )

    order_line = fields.One2many(
        comodel_name='back.order.line',
        inverse_name='order_id',
        string="Order Lines",
        copy=True, auto_join=True)

    amount_untaxed = fields.Monetary(
        string="Untaxed Amount",
        store=True,
        compute='_compute_amounts',
        currency_field='currency_id',  # Add the currency_field attribute
        tracking=5
    )
    amount_tax = fields.Monetary(string="Taxes", store=True, compute='_compute_amounts')
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts', tracking=4)
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    fiscal_position_id = fields.Many2one(
        comodel_name='account.fiscal.position',
        string="Fiscal Position",
        # compute='_compute_fiscal_position_id',
        store=True, readonly=False, precompute=True, check_company=True,
        help="Fiscal positions are used to adapt taxes and accounts for particular customers or sales orders/invoices."
             "The default value comes from the customer.",
        domain="[('company_id', '=', company_id)]")

    invoice_id = fields.Many2one('account.move', readonly=True, string="Invoice Number")
    invoice_ids = fields.Many2many('account.move')
    agent_invoice_ids = fields.Many2many('account.move', 'order_id')
    invoice_date = fields.Datetime(string="Invoice Date", readonly=True, compute="_compute_invoice_date")
    sales_agent_id = fields.Many2one('res.partner', stirng="Sales Agent", domain=[('agent_rank', '>', 0)])
    sale_type = fields.Selection(
        selection=[
            ('retail', "Retail"),
        ],
        string="Sale Type",
        readonly=True, copy=False, index=True,
        tracking=3,
        default='retail')

    freight_charge = fields.Float()
    user_id = fields.Many2one(
        'res.users', string='Salesperson', index=True, tracking=2, default=lambda self: self.env.user,
        domain=lambda self: "[('groups_id', '=', {}), ('share', '=', False), ('company_ids', '=', company_id)]".format(
            self.env.ref("sales_team.group_sale_salesman").id
        ), )
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'sale')], required=True,
                                 compute="_compute_journal_id", store=True, readonly=False)
    agent_journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'purchase')])

    tax_totals_json = fields.Char(compute='_compute_tax_totals_json')
    note = fields.Html('Terms and conditions')
    global_discount = fields.Float(string="Order Discount", default=0)
    discount_product_id = fields.Many2one('product.product')
    invoice_count = fields.Integer(compute="_compute_invoice_count")
    agent_invoice_count = fields.Integer(compute="_compute_invoice_count")

    @api.depends('invoice_id', 'invoice_ids')
    def _compute_invoice_count(self):
        for order in self:
            order.invoice_count = len(order.invoice_ids)
            order.agent_invoice_count = len(order.agent_invoice_ids)

    @api.depends('invoice_id', 'invoice_ids')
    def _compute_invoice_date(self):
        for order in self:
            order.invoice_date = False
            if order.invoice_id and order.invoice_id.invoice_date:
                order.invoice_date = order.invoice_id.invoice_date

    @api.depends('company_id')
    def _compute_journal_id(self):
        for order in self:
            order.journal_id = False
            domain = [('company_id', '=', order.company_id.id), ('type', '=', 'sale')]
            journal = self.env['account.journal'].search(domain, limit=1)
            if journal:
                order.journal_id = journal.id

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):
        def compute_taxes(order_line):
            price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
            order = order_line.order_id
            return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty,
                                                         product=order_line.product_id,
                                                         partner=order.partner_shipping_id)

        account_move = self.env['account.move']
        for order in self:
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line,
                                                                                         compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total,
                                                      order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)

    # @api.depends('partner_shipping_id', 'partner_id', 'company_id')
    # def _compute_fiscal_position_id(self):
    #     """
    #     Trigger the change of fiscal position when the shipping address is modified.
    #     """
    #     cache = {}
    #     for order in self:
    #         if not order.partner_id:
    #             order.fiscal_position_id = False
    #             continue
    #         key = (order.company_id.id, order.partner_id.id, order.partner_shipping_id.id)
    #         if key not in cache:
    #             cache[key] = self.env['account.fiscal.position'].with_company(
    #                 order.company_id
    #             ).get_fiscal_position(order.partner_id, order.partner_shipping_id)
    #         order.fiscal_position_id = cache[key]

    def action_confirm(self):
        if not self.partner_id:
            raise ValidationError(_("Add Partner to continue"))
        if not self.order_line:
            raise ValidationError(_("Add a product in order line to continue"))
        if self.sales_agent_id and not self.agent_journal_id:
            raise ValidationError(_("Agent Journal not found please add"))
        self.state = 'confirm'

    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = {
            'move_type': 'out_invoice',
            'narration': self.note,
            'currency_id': self.company_id.currency_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'partner_id': self.partner_invoice_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'partner_bank_id': self.company_id.partner_id.bank_ids.filtered(
                lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id,
            'journal_id': self.journal_id.id,  # company comes from the journal
            'invoice_origin': self.name,
            'invoice_line_ids': [],
            'company_id': self.company_id.id,
        }
        return invoice_vals

    def _prepare_bill(self):
        self.ensure_one()
        bill_vals = {
            'move_type': 'in_invoice',
            'narration': self.note,
            'currency_id': self.company_id.currency_id.id,
            'user_id': self.user_id.id,
            'invoice_user_id': self.user_id.id,
            'partner_id': self.sales_agent_id.id,
            'partner_shipping_id': self.partner_shipping_id.id,
            'partner_bank_id': self.company_id.partner_id.bank_ids.filtered(
                lambda bank: bank.company_id.id in (self.company_id.id, False))[:1].id,
            'journal_id': self.agent_journal_id.id,
            'invoice_origin': self.name,
            'invoice_line_ids': [
                (0, 0, {
                    'product_id': self.sales_agent_id.sale_agent_product_id.id,
                    'price_unit': self.get_agent_commission(),
                    'tax_ids': [(6, 0, self.sales_agent_id.sale_agent_product_id.supplier_taxes_id.ids)],
                    'product_uom_id': self.sales_agent_id.sale_agent_product_id.uom_id.id,
                })],
            'company_id': self.company_id.id,
        }
        return bill_vals

    def get_agent_commission(self):
        commission = self.sales_agent_id.agent_comm
        total = self.amount_total
        amount = (commission / 100) * total
        return amount

    def _create_invoice(self):
        invoice_vals = self._prepare_invoice()
        invoice_line_vals = []
        for line in self.order_line:
            invoice_line_vals.append(
                (0, 0, line._prepare_invoice_line()),
            )
        invoice_vals['invoice_line_ids'] += invoice_line_vals
        move = self.env['account.move'].sudo().create([invoice_vals])
        return move

    def action_create_invoice(self):
        move = self._create_invoice()
        if self.sales_agent_id:
            self.action_agent_bill()
        if move:
            self.invoice_id = move.id
            ids = self.invoice_ids.ids
            self.invoice_ids = ids + [move.id]

    def action_to_draft(self):
        if self.invoice_id:
            self.invoice_id.button_draft()
            self.invoice_id = False
        if self.agent_invoice_ids:
            [x.button_draft() for x in self.agent_invoice_ids if x.state == 'posted']
        self.state = 'draft'

    def _create_agent_bill(self):
        bill_vals = self._prepare_bill()
        move = self.env['account.move'].sudo().create([bill_vals])
        if move:
            ids = self.agent_invoice_ids.ids
            self.agent_invoice_ids = ids + [move.id]
        return move

    def action_agent_bill(self):
        if not self.sales_agent_id:
            raise ValidationError(_("Add sale agent to continue"))
        self._create_agent_bill()

    def action_view_invoices(self):
        return {
            'name': _('Back Office Invoices'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.invoice_ids.ids)]
        }

    def action_view_agent_bill(self):
        return {
            'name': _('Back Office Invoices'),
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'context': "{'move_type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.agent_invoice_ids.ids)]
        }

    @api.onchange('sales_agent_id')
    def onchange_sale_agent_id(self):
        if self.sales_agent_id:
            self.agent_journal_id = self.sales_agent_id.sale_agent_journal_id.id

    @api.onchange('global_discount')
    def onchange_global_discount(self):
        if self.global_discount == 0 or not self.global_discount:
            if self.order_line and [x for x in self.order_line if x.discount_line == True]:
                line = [x for x in self.order_line if x.discount_line == True][0]
                line.price_unit = 0
                line.unlink()
        else:
            if self.global_discount > 0:
                if self.amount_total < self.global_discount:
                    raise ValidationError(_("Discount amount must be less than Total Amount"))
                if self.order_line and [x for x in self.order_line if x.discount_line == True]:
                    line = [x for x in self.order_line if x.discount_line == True][0]
                    line.price_unit = - self.global_discount
                else:
                    if not self.discount_product_id:
                        raise ValidationError(_("Add Discount Product"))
                    orderline = []
                    orderline.append([0, 0, {'product_id': self.discount_product_id.id,
                                             'price_unit': - self.global_discount,
                                             'discount_line': True}])
                    self.order_line = orderline

    @api.depends('order_line.price_total', 'global_discount')
    def _compute_amounts(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
            })

    # @api.depends('order_line.price_subtotal', 'order_line.price_tax', 'order_line.price_total')
    # def _compute_amounts(self):
    #     """Compute the total amounts of the SO."""
    #     for order in self:
    #         order_lines = order.order_line.filtered(lambda x: not x.display_type)
    #
    #         if order.company_id.tax_calculation_rounding_method == 'round_globally':
    #             tax_results = self.env['account.tax']._compute_taxes([
    #                 line._convert_to_tax_base_line_dict()
    #                 for line in order_lines
    #             ])
    #             totals = tax_results['totals']
    #             amount_untaxed = totals.get(order.currency_id, {}).get('amount_untaxed', 0.0)
    #             amount_tax = totals.get(order.currency_id, {}).get('amount_tax', 0.0)
    #         else:
    #             amount_untaxed = sum(order_lines.mapped('price_subtotal'))
    #             amount_tax = sum(order_lines.mapped('price_tax'))
    #
    #         order.amount_untaxed = amount_untaxed
    #         order.amount_tax = amount_tax
    #         order.amount_total = order.amount_untaxed + order.amount_tax

    @api.depends('partner_id')
    def _compute_partner_invoice_id(self):
        for order in self:
            order.partner_invoice_id = order.partner_id.address_get(['invoice'])[
                'invoice'] if order.partner_id else False

    @api.depends('partner_id')
    def _compute_partner_shipping_id(self):
        for order in self:
            order.partner_shipping_id = order.partner_id.address_get(['delivery'])[
                'delivery'] if order.partner_id else False


class BackOrderLine(models.Model):
    _name = 'back.order.line'
    _description = 'Back Order Lines'

    order_id = fields.Many2one('office.order', string='Order', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    product_uom_qty = fields.Float(string='Quantity', required=True, default='1.0')
    price_unit = fields.Float(
        string="Unit Price",
        digits='Product Price', compute='_compute_price_unit',
        store=True, readonly=False, required=True, precompute=True)

    product_code = fields.Char(string="Code", related='product_id.default_code')

    discount = fields.Float(
        string="Discount (%)",
        digits='Discount',
        store=True, readonly=False, precompute=True)

    # Pricing fields
    tax_id = fields.Many2many(
        comodel_name='account.tax',
        string="Taxes",
        store=True, readonly=False, precompute=True,
        compute='_compute_tax_id',
        context={'active_test': False},
        check_company=True)

    price_subtotal = fields.Monetary(
        string="Subtotal",
        store=True, precompute=True, compute='_compute_amount')
    price_tax = fields.Float(
        string="Total Tax", compute="_compute_amount",
        store=True, precompute=True)
    price_total = fields.Monetary(
        string="Total", compute="_compute_amount",
        store=True, precompute=True)

    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        related='uom_id.id',
        store=True, readonly=False, precompute=True, ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]")

    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', depends=['product_id'])

    company_id = fields.Many2one(
        related='order_id.company_id',
        store=True, index=True, precompute=True)

    currency_id = fields.Many2one(
        related='order_id.currency_id',
        depends=['order_id.currency_id'],
        store=True, precompute=True)

    product_uom = fields.Many2one(
        comodel_name='uom.uom',
        string="Unit of Measure",
        store=True, readonly=False, precompute=True, ondelete='restrict',
        domain="[('category_id', '=', product_uom_category_id)]")
    discount_line = fields.Boolean()
    display_type = fields.Selection(
        selection=[
            ('line_section', "Section"),
            ('line_note', "Note"),
        ],
        default=False)

    @api.depends('product_id', 'company_id')
    def _compute_tax_id(self):
        taxes_by_product_company = defaultdict(lambda: self.env['account.tax'])
        lines_by_company = defaultdict(lambda: self.env['back.order.line'])
        cached_taxes = {}
        for line in self:
            lines_by_company[line.company_id] += line
        for product in self.product_id:
            for tax in product.taxes_id:
                taxes_by_product_company[(product, tax.company_id)] += tax
        for company, lines in lines_by_company.items():
            for line in lines.with_company(company):
                taxes = taxes_by_product_company[(line.product_id, company)]
                if not line.product_id or not taxes:
                    # Nothing to map
                    line.tax_id = False
                    continue
                fiscal_position = line.order_id.fiscal_position_id
                cache_key = (fiscal_position.id, company.id, tuple(taxes.ids))
                if cache_key in cached_taxes:
                    result = cached_taxes[cache_key]
                else:
                    result = fiscal_position.map_tax(taxes)
                    cached_taxes[cache_key] = result
                # If company_id is set, always filter taxes by the company
                line.tax_id = result

    # @api.depends('product_id', 'product_uom', 'product_uom_qty')
    # def _compute_price_unit(self):
    #     for rec in self:
    #         if rec.product_id:
    #             rec.price_unit = rec.product_id.list_price
    #             rec.price_subtotal = rec.product_id.list_price * rec.product_uom_qty
    #             rec.price_total = rec.price_subtotal - rec.discount

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        self.price_unit = self.product_id.lst_price
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            self.update({
                'product_uom': self.product_id.uom_id,
                'product_uom_qty': self.product_uom_qty or 1.0
            })

        # self._update_description()
        self._update_taxes()

        product = self.product_id
        if product and product.sale_line_warn != 'no-message':
            if product.sale_line_warn == 'block':
                self.product_id = False
            return {
                'warning': {
                    'title': _("Warning for %s", product.name),
                    'message': product.sale_line_warn_msg,
                }
            }

    def _update_taxes(self):
        if not self.product_id:
            return

        self._compute_tax_id()

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.tax_id.compute_all(price, line.order_id.currency_id, line.product_uom_qty,
                                            product=line.product_id, partner=line.order_id.partner_shipping_id)
            line.update({
                'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
            })

    # @api.onchange('discount')
    # def onchange_discount(self):
    #     for rec in self:
    #         rec.price_total = rec.price_subtotal - rec.discount

    def _prepare_invoice_line(self):
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.product_uom_qty,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
        }
        return res
