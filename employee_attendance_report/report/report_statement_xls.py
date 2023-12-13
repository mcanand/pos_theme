from odoo import models
import json
from datetime import datetime,timedelta
from datetime import date
from dateutil import tz


class ResUsers(models.Model):
    _inherit = 'res.users'

    def covert_time_to_user_tz(self, stddatetime):
        user_tz = tz.gettz(self.env.user.tz)
        std_tz = tz.gettz('UTC')
        print('ugtugjg')
        userdatetime = stddatetime.replace(tzinfo=std_tz).astimezone(user_tz).replace(tzinfo=None)
        return userdatetime


class CollectionSaleReportXls(models.AbstractModel):
    _name = 'report.employee_attendance_report.attendance_xls'
    _inherit = 'report.report_xlsx.abstract'



    def generate_xlsx_report(self, workbook, data, lines):
        # company_id = self.env['res.company'].browse(data['company'])
        sheet1 = workbook.add_worksheet("Daily Attendance Report")
        main_head = workbook.add_format({
            'align': 'center',
            'valign': 'vcenter',
            'top': 1,
            'left': 1,
            'bg_color': '#9fc5e8',
            'font_color': '#3d85c6',
            'font_size': 18,
            'bold': 1,
        })

        sub_heading = workbook.add_format({
            'font_size': 11,
            'align': 'vcenter',
            'font_color': '#f3f6f4',
            'bold': 1,
            'bg_color': '#3d85c6',

        })

        total_head = workbook.add_format({
            'font_size': 8,
            'align': 'vcenter',
            'bold': 1,
            # 'bg_color': '#7C7BADBD',

            'bg_color': '#7f8185',
            'font_color': '#0a0a0a',

        })



        sub_total_head = workbook.add_format({
            'font_size': 11,
            'align': 'vcenter',
            'bold': 1,
            # 'bg_color': '#7C7BADBD',

            'font_color': '#181819',

        })
        format3 = workbook.add_format({'font_size': 10, 'align': 'center', 'bold': True})




        format2 = workbook.add_format({
            'font_size': 12,
            'align': 'vcenter',
            'bg_color': '#eeeeee',
        })
        format4= workbook.add_format({
            'font_size': 12,
            'align': 'vcenter',
        })
        format5 = workbook.add_format({
            'font_size': 12,
            'align': 'vcenter',
            'bg_color': '#9fc5e8',

        })

        sheet1.merge_range('B1:G2', "Daily Attendance Report", main_head)
        if lines.from_date==lines.to_date:
            from_date = lines.from_date.strftime('%d/%m/%Y') if lines.from_date else ''
            sheet1.write(6, 1, 'Date :' + from_date, format3)
        else:
            sheet1.write(6, 1, 'From', format3)
            from_date = lines.from_date.strftime('%d/%m/%Y') if lines.from_date else ''
            sheet1.write(6, 2, from_date, format3)
            sheet1.write(6, 3, 'To', format3)
            to_date = lines.to_date.strftime('%d/%m/%Y') if lines.to_date else ''
            sheet1.write(6, 4, to_date, format3)
        # partner_id = self.env['res.partner'].browse(lines.partner_id.id)
        sheet1.set_column(1, 1, 25)
        sheet1.set_column(2, 2, 25)
        sheet1.set_column(3, 3, 25)
        sheet1.set_column(4, 4, 25)
        sheet1.set_column(5, 5, 25)

        #
        # sheet1.write(4, 0, 'Customer', sub_heading)
        # sheet1.write(4, 1, partner_id.name, sub_heading)
        # sheet1.write(5, 0, 'Address', sub_heading)
        # sheet1.write(5, 1, partner_id.street, format2)
        if lines.employee_id:
            rec_data = self.env['hr.attendance'].search(
                [('employee_id', '=', lines.employee_id.id),
                 ('create_date', '>=', lines.from_date),
                 ('create_date', '<=', lines.to_date)
                 ],
            )
        else:
            rec_data = self.env['hr.attendance'].search(
                [
                 ('create_date', '>=', lines.from_date),
                 ('create_date', '<=', lines.to_date)
                 ],
            )
            print(rec_data,'rec_data')

        user = self.env.user
        j = 10
        sub_total = 0
        # sheet1.write(j, 1, 'SL No', sub_heading)
        sheet1.write(j, 1, 'Employee Name', sub_heading)
        sheet1.write(j, 2, 'Check In', sub_heading)
        sheet1.write(j, 3, 'Check Out', sub_heading)
        sheet1.write(j, 4, 'Regular Hours', sub_heading)
        sheet1.write(j, 5, 'Total Hours', sub_heading)
        # sheet1.write(j, 5, 'Site Name', sub_heading)

        for rec in rec_data:
            print('ghhguhj')
            # sl_no += 1
            t = 1
            j += 1

            user_check_in_date = user.covert_time_to_user_tz(rec.check_in) if rec.check_in else ''
            check_in_date = datetime.strptime(str(user_check_in_date), '%Y-%m-%d %H:%M:%S').strftime(
                '%d-%m-%Y %H:%M:%S') if user_check_in_date else ''
            sheet1.write(j, t, rec.employee_id.name, format2)
            t += 1
            sheet1.write(j, t, check_in_date, format2)
            t += 1
            user_check_out_date = user.covert_time_to_user_tz(rec.check_out) if rec.check_out else ''
            check_out_date = datetime.strptime(str(user_check_out_date), '%Y-%m-%d %H:%M:%S').strftime(
                '%d-%m-%Y %H:%M:%S') if user_check_out_date else ''
            sheet1.write(j, t, check_out_date, format2)
            t += 1
            total_hours_timedelta = timedelta(hours=rec.employee_id.resource_calendar_id.hours_per_day)
            formatted_total_hours = str(total_hours_timedelta).split('.')[0]
            sheet1.write(j, t, formatted_total_hours,  format4)
            t += 1
            worked_hours_timedelta = timedelta(hours=rec.worked_hours)
            formatted_worked_hours = str(worked_hours_timedelta).split('.')[0]
            sheet1.write(j, t, formatted_worked_hours,  format5)
        j += 5
        sheet1.write(j,1 , 'SUPERVISOR SIGNATURE',  sub_total_head)
        sheet1.write(j,3 , 'DATE',  sub_total_head)

