# -*- coding: utf-8 -*-
# Part of Odoo, OpenErp. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Transit Text',
    'author': 'Tarek Ibrahim',
    'email': 'tarekmohamedibrahim@gmail.com',
    'version' : '1.1',
    'summary': 'Transit text widget',
    'sequence': 30,
    'description': """
    On your form add the widget 
        <widget name="transtext" ...
    Add in it your text and see it moving on your form
    """,
    'category': 'Tools',
    'website': '',
    'images' : [],
    'depends' : ['base'],
    'data': [
        'views/template.xml',
    ],
    'qweb': [ ],
    'images': [
        'static/description/main_screenshot.png',
    ],
    'license': 'AGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
} 