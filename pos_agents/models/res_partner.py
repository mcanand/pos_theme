from odoo import fields, models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # def _get_journal(self):
    #     journal = self.env.ref('pos_agents.agent_invoice_journal')
    #     return journal.id if journal else ''
    #
    # def _get_product(self):
    #     product =  self.env.ref('pos_agents.agent_commission')
    #     return product.id if product else ''

    agent_rank = fields.Integer(default=0)
    journal_id = fields.Many2one('account.journal', domain=[('type', '=', 'purchase')])
    product_id = fields.Many2one('product.product', domain=[('detailed_type', '=', 'service')])
    agent_comm = fields.Float(string="Agent Commission (%)")
    sale_agent_comm = fields.Float(string="Agent Commission (%)")
