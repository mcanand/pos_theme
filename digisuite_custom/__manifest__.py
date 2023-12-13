# -*- coding: utf-8 -*-

{
    "name": "DigiSuite",
    "version": "15.0.0.0",
    "author": "Dev innovations",
    'summary': 'DigiSuite Custom',
    "description": """""",
    "website": "devinnovations.in",
    "depends": [ 'auth_signup', 'web', 'jazzy_backend_theme', 'fims_login_background_and_styles'],
    "data": [
        'views/auth_signup_login_templates.xml',
        'views/webclient_templates.xml',
        'views/res_config_settings.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'digisuite_custom/static/src/webclient/webclient.js',
            'digisuite_custom/static/src/js/user_menu.js',
        ]
    },

    "auto_install": False,
    "installable": True,

}