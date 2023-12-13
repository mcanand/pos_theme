# -*- coding: utf-8 -*-

{
    'name': 'Employee Documents',
    'version': '15.0.1.0.0',
    'summary': """Manages Employee Documents With Expiry Notifications.""",
    'description': """Manages Employee Related Documents with Expiry Notifications.""",
    'category': 'Generic Modules/Human Resources',
    'author': 'Dev innovations',
    'website': "devinnovations.in",
    'depends': ['base', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_check_list_view.xml',
        'views/employee_document_view.xml',
    ],
    'demo': ['data/data.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
