# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    module_employee_grievance = fields.Boolean(string="Employee Grievance")
    module_employee_promotion = fields.Boolean(string="Employee Promotion")
    module_hr_insurance = fields.Boolean(string="Employee Insurance")
    module_hr_organizational_chart = fields.Boolean(string="Organization Chart")
    module_emp_recruitment = fields.Boolean(string="Recruitment")
    module_employee_training = fields.Boolean(string="Training")

    empl_code_prefix = fields.Char(string="Employee Code Prefix", config_parameter='hr_employee_custom.empl_code_prefix')
    empl_code_suffix = fields.Integer(string="Employee Code", config_parameter='hr_employee_custom.empl_code_suffix')
