# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError,ValidationError
from datetime import date

class EmployeeGrievance(models.Model):
    _name = 'employee.grievance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Grievance")
    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string="Department")
    manager_id = fields.Many2one('hr.employee', related='employee_id.parent_id', string="Manager")
    grievance_subject = fields.Text(string="Grievance Subject")
    grievance_subjects = fields.Char(string="Grievance Subject")
    grievance_desc = fields.Text(string="Grievance Description")
    resolved_on = fields.Date(string="Resolved On")
    rejected_on = fields.Date(string="Rejected On")
    rejection_reason = fields.Text(string="Rejection Reason")
    manager_feedback = fields.Text(string="Manager Feedback")
    rejected_by = fields.Many2one('res.users', string="Rejected BY")
    resolved_by = fields.Many2one('res.users', string="Resolved BY")
    is_employee = fields.Boolean(string="Is Employee", compute="check_employee")
    is_manager = fields.Boolean(string="Is Manager", compute="check_manager")
    is_creator = fields.Boolean(string="Is creator", compute="check_creator")
    state = fields.Selection([('draft', 'Draft'), ('waiting_dm_approval', 'Waiting For DM Approval'), ('approved', 'Approved'),
                              ('rejected', 'Rejected'), ('resolved', 'Resolved')], string="State", default='draft', tracking=True)
    date = fields.Date(string="Created On", default=date.today(), tracking=True)

    def check_creator(self):
        for rec in self:
            rec.is_creator = True if self.env.user == rec.create_uid else False

    def check_employee(self):
        for rec in self:
            rec.is_employee = True if self.env.user == rec.employee_id.user_id else False

    def check_manager(self):
        for rec in self:
            rec.is_manager = True if self.env.user == rec.manager_id.user_id else False

    @api.model
    def create(self, vals):
        res = super(EmployeeGrievance, self).create(vals)
        griev_seq = self.env['ir.sequence'].next_by_code('emp.grievance')
        res.name = griev_seq
        return res

    def get_full_url(self):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        model_name = self._name
        model_id = self.id
        url = base_url + '/web#id=' + str(model_id) + '&model=' + model_name + '&view_type=form'
        return url

    def submit_grievance(self):
        for rec in self:
            rec.state = 'waiting_dm_approval'
            msg = "<p> Dear" + ' ' + rec.manager_id.name + "," + \
                  "<p> Please Approve the grievance" + ' ' + "<b>" + rec.name + ' ' + "</b>" + "against the employee" + ' ' +  "<b>" + "(" + rec.employee_id.name + ")" + "</b>.</p>" + \
                  "<p ><a href =" + rec.get_full_url() + ">" + "Click Here" + "</a>" + ' ' + "for approval.</p>" + \
                  "<br/><p > Thank You </p>" + "<p>" + self.env.user.company_id.name + "</p>"
            msg_id = self.env['mail.mail'].sudo().create({
                'email_from': self.env.user.login,
                'email_to': rec.manager_id.work_email,
                'subject': "Grievance Approve Mail" + ' ' + '-' + ' ' + rec.name,
                'body_html': msg
            })
            if msg_id:
                msg_id.sudo().send()

    def approve_grievance(self):
        for rec in self:
            if not rec.manager_feedback:
                return {
                    "type": "ir.actions.act_window",
                    "name": "Grievance Feedback",
                    "view_mode": "form",
                    "res_model": "grievance.feedback.wiz",
                    "context": {'default_grievance_id': rec.id},
                    "target": "new"
                }
            else:
                rec.sudo().write({'state': 'resolved', 'resolved_by': self.env.user.id, 'resolved_on': date.today()})


    def reject_grievance(self):
        for rec in self:
            if not rec.rejection_reason:
                return {
                    "type": "ir.actions.act_window",
                    "name": "Grievance Rejection Reason",
                    "view_mode": "form",
                    "res_model": "grievance.reject.wiz",
                    "context": {'default_grievance_id': rec.id},
                    "target": "new"
                }
            else:
                rec.sudo().write({'state': 'rejected', 'rejected_by': self.env.user.id, 'rejected_on': date.today()})