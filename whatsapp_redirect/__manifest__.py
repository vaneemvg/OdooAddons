# -*- coding: utf-8 -*-
{
    'name': 'Send Whatsapp Message',
    'version': '13.0.0.0.0',
    'summary': 'Send Message via Whatsapp web',
    'description': 'Send Message via Whatsapp web',
    'category': 'Extra Tools',
    'author': 'Eywa',
    'maintainer': 'Eywa',
    'company': 'Eywa',
    'website': 'https://www.eywa.com.ar',
    'depends': [
        'base','crm'
        ],
    'data': [
        'views/view_crm.xml',
        'views/view_partner.xml',
        'wizard/wizard_partner.xml',
        'wizard/wizard_crm.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'AGPL-3',
}
