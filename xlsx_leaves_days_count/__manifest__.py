# -*- coding: utf-8 -*-
# Part of Odoo, OpenErp. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Leaves Days Count xlsx Report',
    'author': 'Tarek Ibrahim',
    'version' : '1.0',
    'summary': '''Collects the number of days taken by each employees for a specific selected period. it ignores days outside this period''',
    'sequence': 30,
    'description': """
    Excel Report: Leaves Days Count
    Get the defined vacations in the installation, put them as headers in the report
        add the following columns
        1-  serial ( the record # in excel sheet )
        2-  Emp. name
        3-  Vacation Days ( as per vacation type )
        
        Days are count within the selected period only 
        For example, if an employee has taken a vacation
				from 2021-08-30 to 2021-09-02, these are 4 days. In the report if you selected the period from 2021-09-01 to
				2021-09-30, then the report will count 2 days only for this employee.
        Features:
        User can select any / all vacaton types to report
        Manager can change the Headers cells' width, color, and output cell colors
        There is a summary line in the bottom of the collected lines
        below it a 'Total' line that sums all leaves types as days count
        If the user selected only one leave type the 'Total' line won't appear
    """,
    'category': 'Reports',
    'license': 'AGPL-3',
    'website': '',
    'images' : [
        'static/description/icon.png',
        'static/description/popup-screen.png',
        'static/description/sample-output.png',
    ],
    'depends' : [ 'base', 'hr_holidays', ],
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