# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BackEnd Office Operations',
    'version': '1.0.1',
    'category': 'Sales/Point of Sale',
    'sequence': 1,
    'summary': '',
    'description': "",
    'depends': ['point_of_sale',
                'pos_sale',
                'pos_agents',
                'l10n_in',
                'product',
                'account'],
    'data': [
        'security/ir.model.access.csv',
        'views/sessions.xml',
        'views/partner.xml',
        'views/office.xml',
        'views/sequence.xml',

    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
