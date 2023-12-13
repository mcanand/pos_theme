# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import date

class EmployeePromotion(models.TransientModel):
    _name = 'employee.promotion.wiz'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    current_job_id = fields.Many2one('hr.job', string="Current Position")
    new_job_id = fields.Many2one('hr.job', string="Promoted to")

    def update_employee_promotion(self):
        for rec in self:
            rec.employee_id.job_id = rec.new_job_id.id
            vals = {'date': date.today(),
                    'current_job_id': rec.current_job_id.id,
                    'new_job_id': rec.new_job_id.id,
                    'updated_by': self.env.user.id,
                    'employee_id': rec.employee_id.id}
            self.env['emp.promotion.history'].sudo().create(vals)