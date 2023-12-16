# -*- coding: utf-8 -*-
{
    'name': 'CRM Suite',
    'summary': 'CRM Custom',
    'version': '15.0.1.0.0',
    'website': 'devinnovations.in',
    'description': """CRM Custom""",
    'author': 'Dev innovations',
    'installable': True,
    'depends': ['mail', 'base', 'crm', 'crm_iap_enrich', 'sales_team', 'sale_crm','crm_custom','utm'],
    'demo': [
    ],
    'data': [
        'data/crm_lead_seq.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/res_config_setting.xml',
        'views/card_type.xml',
        'views/crm.xml',
        'views/crm_stage.xml',
        'views/lead_refeeral_activity.xml',
        'reports/dsa_report.xml',
        'reports/kyc_report.xml',
        'wizard/reject_wizard.xml',

    ],
    'assets': {

        'web.assets_backend': [
                'crmsuite_custom/static/src/css/digi_crm.css',
            'crmsuite_custom/static/src/scss/list_view.scss'
        ],

    },
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': True,
    'application': True,
}
