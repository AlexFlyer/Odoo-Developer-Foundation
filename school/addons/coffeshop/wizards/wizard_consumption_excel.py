from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class WizardConsumptionExcel(models.TransientModel):
    _name = 'wizard.consumption.excel'
    _description = 'Wizard Consumption Excel'

    carrer_ids = fields.Many2many(comodel_name='coffeshop.carrer', string='Carrers')

    
    def action_generate_excel(self):
        return self.env.ref('coffeshop.action_consumption_excel').report_action(self)



class ReportConsumptionExcel(models.AbstractModel):
    _name = 'report.coffeshop.report_consumption_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, objs):
        sheet = workbook.add_worksheet('Consumptions')
        sheet.write(0, 0, 'Student')
        sheet.write(0, 1, 'Coffeshop')
        sheet.write(0, 2, 'Meal')
        sheet.write(0, 3, 'Date')
        sheet.write(0, 4, 'State')
        row = 1
        for obj in objs:
            consumptions = obj.env['coffeshop.consumption'].search([('carrer_id', 'in', obj.carrer_ids.ids)] if obj.carrer_ids else [])
            for cons in consumptions:
                sheet.write(row, 0, cons.student_id.name)
                sheet.write(row, 1, cons.coffeshop_id.name)
                sheet.write(row, 2, cons.meal_id.name)
                sheet.write(row, 3, str(cons.consumption_date))
                sheet.write(row, 4, cons.state)
                row += 1
