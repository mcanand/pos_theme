# -*- coding: utf-8 -*-

{
    "name" : "Employee Suite",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'Employee Custom',
    "description": """Employee Custom""",
    "website": "devinnovations.in",
    "depends": ['base', 'hr', 'employee_stages', 'employee_check_list', 'hr_skills'],
    "data": [
        'data/hr_employee_cron.xml',
        'security/ir.model.access.csv',
        'views/res_config_settings_views.xml',
        'views/hr_employee.xml',
        'views/hr_employee_config.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_employee_custom/static/components/chatter/chatter.scss',
        ]
    },

    "auto_install": False,
    "installable": True,

}