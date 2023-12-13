# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import date

class GrievanceFeedbackWiz(models.TransientModel):
    _name = 'grievance.feedback.wiz'

    grievance_id = fields.Many2one('employee.grievance', string="Grievance")
    manager_feedback = fields.Text(string="Manager's Feedback")

    def update_manager_feedback(self):
        for rec in self:
            rec.grievance_id.sudo().write({'state': 'resolved',
                                           'resolved_by': self.env.user.id,
                                           'resolved_on': date.today(),
                                           'manager_feedback': rec.manager_feedback})



class GrievanceRejectionWiz(models.TransientModel):
    _name = 'grievance.reject.wiz'

    grievance_id = fields.Many2one('employee.grievance', string="Grievance")
    rejection_reason = fields.Text(string="Rejection Reason")

    def update_rejection_reason(self):
        for rec in self:
            rec.grievance_id.sudo().write({'state': 'rejected',
                                           'rejected_by': self.env.user.id,
                                           'rejected_on': date.today(),
                                           'rejection_reason': rec.rejection_reason})


