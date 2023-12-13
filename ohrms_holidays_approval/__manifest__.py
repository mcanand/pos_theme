# -*- coding: utf-8 -*-

{
    'name': 'Leave Multi-Level Approval',
    'version': '15.0.1.0.0',
    'summary': """Multilevel Approval for Leaves""",
    'description': 'Multilevel Approval for Leaves, leave approval, multiple leave approvers, leave, approval',
    'category': 'Generic Modules/Human Resources',
    'author': 'Dev Innovations',
    'company': 'Dev Innovations',
    'website': "www.devinnovations.in",
    'depends': ['base_setup', 'hr_holidays'],
    'data': [
        'views/leave_request.xml',
        'security/ir.model.access.csv',
        'security/security.xml'
    ],
    'images': ['static/description/bannerr.png'],
    'license': "AGPL-3",
    'installable': True,
    'auto_install': False,
    'application': False,
}
