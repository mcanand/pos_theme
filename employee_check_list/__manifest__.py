# -*- coding: utf-8 -*-

{
    'name': 'Employee Checklist',
    'version': '15.0.1.0.0',
    'summary': """Manages Employee's Entry & Exit Process""",
    'description': """This module is used to remembering the employee's entry and exit progress.""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Dev innovations',
    'website': "devinnovations.in",
    'depends': ['base', 'employee_documents_expiry'],
    'data': [
        'views/employee_form_inherit_view.xml',
        'views/checklist_view.xml',
        # 'views/settings_view.xml',
    ],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}

