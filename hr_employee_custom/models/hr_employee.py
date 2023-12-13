# -*- coding: utf-8 -*-
from odoo import models, fields, api,_
from datetime import datetime, date


class EmployeeFormInherit(models.Model):
    _inherit = 'hr.employee'

    employee_code = fields.Char(string="Employee ID")
    coach_id = fields.Many2one(
        'hr.employee', 'Deapartment Head', compute='_compute_coach', store=True, readonly=False,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        help='Select the "Employee" who is the coach of this employee.\n'
             'The "Coach" has no specific rights or responsibilities by default.')
    home_country_street = fields.Char(string="Address")
    home_country_street2 = fields.Char(string="Street2")
    home_country_city = fields.Char(string="City")
    home_country_state_id = fields.Many2one('res.country.state', string=" State", domain="[('country_id', '=?', home_address_country_id)]")
    home_country_zip = fields.Char(string="Zip",)
    home_address_country_id = fields.Many2one('res.country', string="Country")
    home_country_phone = fields.Char('Contact Number')

    local_street = fields.Char(string="Address")
    local_street2 = fields.Char(string="Street2")
    local_city = fields.Char(string="City")
    local_state_id = fields.Many2one('res.country.state', string=" State",
                                            domain="[('country_id', '=?', local_country_id)]")
    local_zip = fields.Char(string="Zip", )
    local_country_id = fields.Many2one('res.country', string="Country")
    local_phone = fields.Char('Contact Number')
    local_email = fields.Char(string="Email")
    is_manager = fields.Boolean(string="Manager")
    is_hod = fields.Boolean(string="Department Head")
    employee_type_id = fields.Many2one('hr.emp.type', string="Employee Type")
    emp_education_line_id = fields.One2many('employee.education.line', 'employee_id', string="Education Details")

    @api.model
    def create(self, vals):
        res = super(EmployeeFormInherit, self).create(vals)
        config_settings = self.env['res.config.settings'].search([], limit=1, order="id desc")
        code_prefix = self.env['ir.config_parameter'].sudo().get_param('hr_employee_custom.empl_code_prefix')
        code_suffix = self.env['ir.config_parameter'].sudo().get_param('hr_employee_custom.empl_code_suffix')
        # config_settings_values = config_settings.empl_code_prefix + '/'+str(config_settings.empl_code_suffix)
        config_settings_values = code_prefix + '/' + str(code_suffix)
        self.env['ir.config_parameter'].sudo().set_param('hr_employee_custom.empl_code_suffix', (int(code_suffix)+1))
        res.employee_code = config_settings_values
        return res

    def get_birthday_date(self, dob):
        date_obj = datetime.strptime(str(dob), '%Y-%m-%d')
        if date_obj.day >= 10 and date_obj.day <= 20:
            ordinal_suffix = 'th'
        else:
            v = date_obj.day % 10  # to get the remainder of the operation
            if v == 1:
                ordinal_suffix = 'st'
            elif v == 2:
                ordinal_suffix = 'nd'
            elif v == 3:
                ordinal_suffix = 'rd'
            else:
                ordinal_suffix = 'th'

        # format 'July 3rd'
        return datetime.strftime(date_obj, '%-d' + ordinal_suffix + ' ' + '%B')

    @api.model
    def get_emp_bday_notification(self):
        employees = self.env['hr.employee'].sudo().search([]).filtered(lambda s: s.birthday ==  date.today())
        for emp in employees:
            if emp.birthday and emp.parent_id and emp.parent_id.user_id:
                birth = datetime.strptime(str(emp.birthday), "%Y-%m-%d").date()
                today = date.today()
                if birth.day == today.day and birth.month == today.month:
                    user = emp.parent_id.user_id
                    emp_dob = emp.get_birthday_date(emp.birthday)
                    msg = "Employee %s's birthday is on %s." %(emp.name, emp_dob)
                    MailChannel = self.env(context=user.context_get())['mail.channel']
                    print("Channel", MailChannel.browse(MailChannel.channel_get([user.partner_id.id])['id']))
                    msg = "<p>"+msg+"</p>"
                    MailChannel.browse(MailChannel.channel_get([user.partner_id.id])['id']) \
                        .message_post(
                        body=_(msg),
                        message_type='comment',
                        subtype_xmlid='mail.mt_comment'
                    )


class EmployeeEqucationLine(models.Model):
    _name = 'employee.education.line'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    degree_id = fields.Many2one('hr.edu.qualification', string="Degree")
    emp_field_study = fields.Char(string="Field Of Study")
    education_school = fields.Char(string="School")
    education_certificate_id = fields.Many2many('ir.attachment', string="Certificate")