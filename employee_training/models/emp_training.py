# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import date

class EmployeeTraining(models.Model):
    _name = 'employee.training'

    training_pgm = fields.Char(string="Trainig Program")
    training_course = fields.Many2one('training.course', string="Course")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    state = fields.Selection([('Ongoing', 'Ongoing'), ('Completion', 'Completion')], string="Status", default='Ongoing')
    employee_id = fields.Many2one('hr.employee', string="Employee")



class TrainingCourse(models.Model):
    _name = 'training.course'

    name = fields.Char(string="Course")

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    training_line_ids = fields.One2many('employee.training', 'employee_id', string="Training")

