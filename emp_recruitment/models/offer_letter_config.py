# -*- coding: utf-8 -*-
from odoo import fields, models, api, _

class OfferLetterConfig(models.Model):
    _name = 'offer_letter.config'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Name", default="Offer Letter Details")
    offer_letter_details = fields.Html(string="Offer Letter Details")

class SalaryType(models.Model):
    _name = 'salary.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    salary_type = fields.Char(string="Name")

    def name_get(self):
        result = []
        for rec in self:
            name = rec.salary_type if rec.salary_type else 'Salary Type'
            result.append((rec.id, name))
        return result
