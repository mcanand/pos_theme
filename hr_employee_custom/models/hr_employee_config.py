# -*- coding: utf-8 -*-
from odoo import models, fields, api


class EducationQualification(models.Model):
    _name = 'hr.edu.qualification'


    name = fields.Char(string="Qualification")


class HrEmployeeType(models.Model):
    _name = 'hr.emp.type'

    name = fields.Char(string="Employee Type")
