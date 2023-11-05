from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'


    def _get_journal(self):
        return self.env.ref('pos_agents.gent_invoice_journal').id
    def _get_product(self):
        return self.env.ref('pos_agents.agent_commission').id

    agent_rank = fields.Integer(default=0)
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'purchase')], default=_get_journal)
    product_id = fields.Many2one('product.product', default=_get_product, readonly=True)
    agent_comm = fields.Float(string="Agent Commission (%)")

