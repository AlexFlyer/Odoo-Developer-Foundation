# -*- coding: utf-8 -*-
import logging
from odoo import models, fields, api
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WizardConsumptionExcel(models.TransientModel):
    _name = 'wizard.consumption.excel'

    carrer_ids = fields.Many2many(comodel_name='carrer', required=True)
    state = fields.Selection(selection=[
            ('draft', 'Draft'),
            ('delivered', 'Delivered'),
            ('cancelled', 'Cancelled'),
        ], default='draft')

    def action_print_report(self):
        return self.env.ref('coffee_shop.action_consumption_excel').report_action(self)


class ReportConsumptionExcel(models.AbstractModel):
    _name = 'report.coffee_shop.report_consumption_excel'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, ctx, data):
        sheet = workbook.add_worksheet('PESTAÑA')

        sheet.write(0, 0, 'Especialidad')
        sheet.write(0, 1, 'Platillo')
        sheet.write(0, 2, 'Cuenta')

        row = 1

        for esp in data.carrer_ids:
            self.env.cr.execute("""
                    SELECT 
                        car.name AS carrer, 
                        m.name AS meal,
                        COUNT(con.meal_id) AS c_meal
                    FROM carrer AS car
                    INNER JOIN student AS std ON car.id = std.carrer_id
                    INNER JOIN consumption AS con ON std.id = con.student_id
                    INNER JOIN meal AS m ON con.meal_id = m.id
                    WHERE car.id = %s
                    GROUP BY car.name, m.name
                    ORDER BY c_meal DESC
                    LIMIT 1
                """, (esp.id,))

            res = self.env.cr.dictfetchone()

            if not res:
                sheet.write(row, 0, esp.name)
                sheet.write(row, 1, '')
                sheet.write(row, 2, '')
            else:
                sheet.write(row, 0, res['carrer'])
                sheet.write(row, 1, res['meal'])
                sheet.write(row, 2, res['c_meal'])
            row += 1

        # sheet.write(0, 0, 'Nombre Consumo')
        # sheet.write(0, 1, 'Alumno')
        # sheet.write(0, 2, 'Dia')
        # sheet.write(0, 3, 'Cafeteria')
        # sheet.write(0, 4, 'Platillo')
        # sheet.write(0, 5, 'Precio')

        # row = 1

        # for consumo in data:
        #     sheet.write(row, 0, consumo.display_name)
        #     sheet.write(row, 1, consumo.alumno_id.name)
        #     sheet.write(row, 2, consumo.dia)
        #     sheet.write(row, 3, consumo.cafeteria_id.name)
        #     sheet.write(row, 4, consumo.platillo_id.name)
        #     sheet.write(row, 5, consumo.platillo_id.precio)

        #     row += 1
