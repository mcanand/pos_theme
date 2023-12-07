from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    themes = fields.Selection([('default', 'Default'), ('theme_new', 'New Theme')], default='theme_new')
    fast_payment_method_id = fields.Many2one('pos.payment.method', required=True)
    freight_charge = fields.Float()
    auto_invoice = fields.Boolean()
    agent_ids = fields.Many2many('res.partner', domain=[('agent_rank', '>', 0)], string='Agents')
    global_discount = fields.Boolean()
    disc_product_id = fields.Many2one('product.product', string="Discount Product")
