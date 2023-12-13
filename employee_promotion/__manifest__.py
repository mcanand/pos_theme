# -*- coding: utf-8 -*-

{
    "name": "Employee Promotion",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'Employee Promotion',
    "description": """Employee Job Promotion""",
    "website": "devinnovations.in",
    "depends": ['base', 'mail', 'hr'],
    "data": [
        'security/ir.model.access.csv',
        'views/hr_employee.xml',
        'wizard/employee_promotion_wiz.xml',
    ],

    "auto_install": False,
    "installable": True,

}