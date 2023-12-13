# -*- coding: utf-8 -*-
{
    'name': "Attendance Report",

    'summary': """
        Attendance  Report""",

    'description': """
       Attendance Report
    """,

    'author': "",
    'website': "",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_attendance','web','report_xlsx',],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
'report/report_pdf.xml',
        'wizard/customer_report_wizard_view.xml',
        'views/attendance.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
