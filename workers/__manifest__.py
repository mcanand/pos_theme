
{
    'name': 'workers',
    'version': '15.0.0.1.0.1',
    'category': '',
    'sequence': 1,
    'summary': '',
    'description': "To find workers in the current location",
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/profession_category.xml',
        'views/worker_profession.xml',
        'views/partner.xml',
    ],
    'installable': True,
    'application': True,
    'assets': {

    },
    'license': 'LGPL-3',
}
