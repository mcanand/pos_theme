# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    emp_promotion_history_ids = fields.One2many('emp.promotion.history', 'employee_id', string="Promotion History")

    def emp_job_position_update(self):
        for rec in self:
            return {
                "type": "ir.actions.act_window",
                "name": "Employee Job Promotion",
                "view_mode": "form",
                "res_model": "employee.promotion.wiz",
                "context": {'default_employee_id': rec.id, 'default_current_job_id': rec.job_id.id if rec.job_id else ''},
                "target": "new"
            }

class EmpPromotionHistory(models.Model):
    _name = 'emp.promotion.history'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    current_job_id = fields.Many2one('hr.job', string="Promotion From")
    new_job_id = fields.Many2one('hr.job', string="Promoted to")
    date = fields.Date(string="Date")
    updated_by = fields.Many2one('res.users', string="Promoted By")

