# -*- coding: utf-8 -*-
# Part of Odoo, OpenErp. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Leaves Days Count xlsx Report',
    'author': 'Tarek Ibrahim',
    'version' : '1.0',
    'summary': 'Leaves Days Count xlsx Report',
    'sequence': 30,
    'description': """
    Excel Report: Leaves Days Count
   Get the defined vacations in the installation, put them as headers in the report
        add the following columns
        1-  serial ( the record # in excel sheet )
        2-  Emp. name
        3-  Vacation Days ( as per vacation type )
        
        Note: 
        Days are count within the selected period only 
        ex. suppose the report filter from 2021-09-01 to 2021-09-10 and an employee has been taken a vacation from 2021-08-25 to 2021-09-05 the report will count only 5 days for this employee
        
        Features:
        User can select any / all vacaton types to report
        Manager can change the Headers cells' width, color, and output cell colors
        There is a summary line in the bottom of the collected lines
        below it a 'Total' line that sums all leaves types as days count
        If the user selected only one leave type the 'Total' line won't appear
        
    """,
    'category': 'Reports',
    'website': '',
    'images' : [],
    'depends' : [
        'base',
        'hr_holidays',
                 ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'wizard/xlsx_leaves_days_count_view.xml',
    ],
    'demo': [ ],
    'installable': True,
    'application': False,
    'auto_install': False,
} 