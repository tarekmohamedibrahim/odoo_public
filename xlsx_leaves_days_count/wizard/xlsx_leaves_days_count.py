# -*- coding: utf-8 7*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models,_
from odoo.exceptions import ValidationError
import xlsxwriter
from io import BytesIO
import base64
import string
from datetime import timedelta, datetime, date
from dateutil.relativedelta import relativedelta
from collections import defaultdict


class xlsx_leaves_days_count(models.TransientModel):
    _name = 'xlsx.leaves.days.count'

    content = fields.Binary('Content')
    date_from = fields.Date('From')
    date_to = fields.Date('To')
    hr_leave_type = fields.Many2many('hr.leave.type')
    state = fields.Selection([ ('draft', 'To Submit'),
                                ('cancel', 'Cancelled'),
                                ('confirm', 'To Approve'),
                                ('refuse', 'Refused'),
                                ('validate1', 'Second Approval'),
                                ('validate', 'Approved')],
                             string='Status', default='validate')
    #changable settings
    right_to_left = fields.Boolean('Right To Left')
    protect = fields.Boolean('Readonly', default=True)
    cell_width = fields.Integer(default=25)
    header_color = fields.Char(default='#ccffff')
    cell_color = fields.Char(default='white')

    @api.model
    def default_get(self, fields):
        res = super(xlsx_leaves_days_count, self).default_get(fields)
        res['hr_leave_type'] = self.env['hr.leave.type'].search([]).ids
        res['date_from'] = str(date.today())[:8]+'01'
        res['date_to'] = str(datetime.strptime(str(date.today())[:8] + '01', '%Y-%m-%d') + relativedelta(months=1, days=-1))[:10]
        return res

    def action_report(self):
        self.ensure_one()

        #Data Collection
        if self.hr_leave_type.ids:
            leave_types = self.hr_leave_type
        else:
            leave_types = self.env['hr.leave.type'].search([])

        emp_leave = defaultdict(lambda: defaultdict(int))
        emp_weekdays = defaultdict(set)
        summary = defaultdict(int)

        #exclude only leaves that are completly out of the selected period
        leave_criteria = [('holiday_status_id', 'in', leave_types.ids),
                          ('state','=',self.state),
                          ('date_to', '>=', str(self.date_from)),
                          ('date_from', '<=', str(self.date_to)+' 23:59:59')]
        leaves = self.env['hr.leave'].search(leave_criteria)

        #get all days representing the criteria
        sdate = self.date_from
        edate = self.date_to
        criteria_days = [str(sdate+timedelta(days=x)) for x in range((edate-sdate).days)]

        #then sum the number of intersecting days per leave per employee per leave
        # N.B: Consider excluding the weekends from thre resource calendar
        for leave in leaves:
            emp_weekdays[leave.employee_id.id] |= {int(res.dayofweek) for res in leave.employee_id.resource_calendar_id.attendance_ids}
            sdate = leave.date_from
            edate = leave.date_to
            leave_days = [str(sdate+timedelta(days=x))[:10] for x in range((edate-sdate).days+1) if (sdate+timedelta(days=x)).weekday() in emp_weekdays[leave.employee_id.id]]
            count_days = len(set(criteria_days) & set(leave_days))
            emp_leave[leave.employee_id.id][leave.holiday_status_id.id] += count_days
            summary[leave.holiday_status_id.id] += count_days

        #Output
        #define output fields
        fields = [
            {'width': 5, 'format': {}, 'title': 'S#'},
            {'width': 25, 'format': {}, 'title': 'Name'},
        ]
        for type in leave_types:
            fields.append(
                {'width': self.cell_width, 'format': {'border':1, 'align': 'center', 'valign': 'vcenter', 'fg_color': self.cell_color}, 'title': type.name},
            )

        #define the xlsx sheet
        _log = BytesIO()
        wb = xlsxwriter.Workbook(_log, {'in_memory': True})
        _output = wb.add_worksheet('Leaves Days Count')

        #general settings changed by the manager, if needed
        if self.right_to_left: _output.right_to_left()
        if self.protect: _output.protect()
        _output.freeze_panes(2, 2)

        #define the header criteria info
        header_format = wb.add_format({'bold': 1, 'border': 1, 'align': 'center', 'valign': 'vcenter', 'fg_color': self.header_color })
        _output.merge_range('A1:B1', 'Leave Days Count', header_format)
        to_column = string.ascii_uppercase[len(leave_types)+1]
        if to_column=='C':
            _output.write(0, 2, '{}, {}'.format(self.date_from, self.date_to), header_format)
        else:
            _output.merge_range('C1:{}1'.format(to_column), 'Between {} and {}'.format(self.date_from, self.date_to), header_format)

        #define the header fields titles
        _row = 1
        cell_format = []
        for i, fld in enumerate(fields):
            _output.set_column('{0}:{0}'.format(string.ascii_uppercase[i]), fld['width'])
            cell_format.append(wb.add_format(fld['format']))
            _output.write(_row, i, fld['title'], header_format)
        _row+=1

        #collect the list to output from
        criteria = res = []
        serial = 1
        for emp in self.env['hr.employee'].search(criteria):
            if not emp_leave.get(emp.id):
                continue
            elm = []
            elm.append(serial)
            elm.append(getattr(emp,'name'))
            for type in leave_types:
                elm.append(emp_leave[emp.id].get(type.id) or '')
            res.append(elm)
            serial+=1

        if not res:
            raise ValidationError(_('There is no data to output!'))

        #Writing the Output
        for ln in res:
            for _col, val in enumerate(ln):
                _output.write(_row, _col, val, cell_format[_col])
            _row+=1

        #Writing the Summary
        _row += 1
        _output.merge_range('A{0}:B{0}'.format(_row+1),'Summary:', header_format)
        for _col, type in enumerate(leave_types):
            _output.write(_row, _col+2, summary.get(type.id), header_format)
        if len(leave_types)>1:
            _output.merge_range('A{0}:B{0}'.format(_row+3),'Total:', header_format)
            _output.write(_row+2, 2, sum(summary.get(type.id) or 0 for type in leave_types), header_format)

        #closing
        wb.close()
        _log.seek(0)
        content = _log.read()
        _log.close()
        self.write({'content': base64.encodebytes(content)})
        return {
            'type': 'ir.actions.act_url',
            'url':'web/content/?model={}&field=content&download=true&id={}&filename=leaves_days_count.xlsx'.format(self._name, self.id),
            'target': 'new',
        }