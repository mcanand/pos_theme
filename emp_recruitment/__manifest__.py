# -*- coding: utf-8 -*-

{
    "name": "Recruitment",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'Custom Recruitment module for generating the employee offer letter',
    "description": """""",
    "website": "devinnovations.in",
    "depends": ['base', 'mail', 'web', 'hr', 'employee_stages'],
    "data": [
        'security/ir.model.access.csv',
        'views/offer_letter_config.xml',
        'views/emp_offer_letter.xml',
        'views/hr_employee.xml',
        'views/menu.xml',
        'report/emp_offer_letter.xml',
    ],
    "auto_install": False,
    "installable": True,

}