# -*- coding: utf-8 -*-
{
    'name': 'country extra locations',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'add districts, Location',
    'description': """add districts and location for states""",
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/district.xml',
        'views/location.xml',
        'views/res_partner.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
