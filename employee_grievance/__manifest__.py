# -*- coding: utf-8 -*-

{
    "name" : "Grievance",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'Employee Grievance',
    "description": """Employee Grievance""",
    "website": "devinnovations.in",
    "depends": ['base', 'mail', 'hr'],
    "data": [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/employee_grievance.xml',
        'views/menu.xml',
        'wizard/grievance_feedback_wiz.xml',
    ],

    "auto_install": False,
    "installable": True,

}