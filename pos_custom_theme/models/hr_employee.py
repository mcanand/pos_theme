from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    show_info = fields.Boolean(string="Show Product Info")