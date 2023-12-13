# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    emp_code_prefix = fields.Char(string="Employee Code Prefix", config_parameter='digisuite_custom.emp_code_prefix')
    emp_code_suffix = fields.Integer(string="Employee Code",  config_parameter='digisuite_custom.emp_code_suffix')
