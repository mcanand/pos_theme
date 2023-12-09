# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    def get_employee_stage_action(self):
        for rec in self:
            emp_offer = self.env['emp.offer_letter'].sudo().search([('employee_id', '=', rec.id)], limit=1)
            if emp_offer.state == 'accepted':
                return {
                    "type": "ir.actions.act_window",
                    "name": "Set as Employee",
                    "view_mode": "form",
                    "res_model": "wizard.employee.stage",
                    "context": {'default_employee_id': rec.id},
                    "target": "new"
                }
            else:
                return {
                    "type": "ir.actions.act_window",
                    "name": "Warning",
                    "view_mode": "form",
                    "res_model": "emp.stage.msg.wiz",
                    "target": "new"
                }

class EmpStageMsgWizWiz(models.TransientModel):

    _name = 'emp.stage.msg.wiz'

    message = fields.Text(default="Employee not accepted the offer letter.")