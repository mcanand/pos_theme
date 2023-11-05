# -*- coding: utf-8 -*-
{
    'name': 'Pos Agents',
    'version': '15.0.0.1',
    'website': '',
    'category': '',
    'author': 'ANAND MC',
    'summary': 'point of sale agents',

    'depends': ['base', 'point_of_sale', 'account'],
    'demo': [

    ],
    'data': [
        'views/agent_journal.xml',
        'views/product.xml',
        'security/ir.model.access.csv',
        'views/pos_partner_agent.xml',
        'views/res_partner.xml',
        'views/pos_orders.xml',
    ],

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
