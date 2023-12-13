# -*- coding: utf-8 -*-

{
    "name" : "Employee Training",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'Employee Training',
    "description": """Employee Grievance""",
    "website": "devinnovations.in",
    "depends": ['base', 'mail', 'hr', 'hr_employee_custom'],
    "data": [
        'security/ir.model.access.csv',
        'views/emp_training.xml',
    ],

    "auto_install": False,
    "installable": True,

}