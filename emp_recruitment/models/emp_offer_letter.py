# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class EmployeeOfferLetter(models.Model):
    _name = 'emp.offer_letter'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string="Employee")
    department_id = fields.Many2one('hr.department', related='employee_id.department_id', string="Department")
    date = fields.Date(string="Date", default=fields.Date.today())
    state = fields.Selection([('draft', 'Draft'), ('accepted', 'Accepted'),
                              ('not_accepted', 'Not Accepted')], default='draft', string="State")
    remuneration_line_ids = fields.One2many('emp.remuneration.line', 'offer_letter_id', string="Remuneration")
    offer_letter_details = fields.Html(string="Offer Letter Details")
    company_id = fields.Many2one('res.company', string="company", default=lambda self: self.env.company)
    job_id = fields.Many2one('hr.job', string="Job Position")

    @api.onchange('employee_id')
    def onchange_employee_id(self):
        for rec in self:
            letter_details = self.env['offer_letter.config'].sudo().search([], limit=1)
            rec.offer_letter_details = letter_details.offer_letter_details
            rec.job_id = rec.employee_id.job_id.id


    def name_get(self):
        result = []
        for rec in self:
            name = rec.employee_id.name if rec.employee_id else 'New'
            result.append((rec.id, name))
        return result

    def offer_accepted(self):
        for rec in self:
            rec.state = 'accepted'

    def offer_not_accepted(self):
        for rec in self:
            rec.state = 'not_accepted'


class RemunerationLine(models.Model):
    _name = 'emp.remuneration.line'

    offer_letter_id = fields.Many2one('emp.offer_letter', string="Offer letter")
    salary_type_id = fields.Many2one('salary.type', string="Salary Type")
    currency_id = fields.Many2one('res.currency', string="Currency")
    salary_break_up = fields.Float(string="Salary Break-Up")
