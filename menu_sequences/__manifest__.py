# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Menu Sequence Digi suite',
    'version': '15.0.0.1',
    'category': 'Sales/Point of Sale',
    'author': 'MC',
    'sequence': 1,
    'summary': '',
    'description': "",
    'depends': ['point_of_sale', 'emp_recruitment', 'website',
                'back_office', 'account', 'mail', 'crm',
                'sale', 'purchase', 'stock', 'hr', 'hr_expense',
                'hr_attendance', 'hr_holidays',
                'contacts'],
    'data': [
        'views/menus.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
