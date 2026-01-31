# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class WizardConsumptionReport(models.TransientModel):
    _name = 'wizard.consumption.report'

    coffee_shop_ids = fields.Many2many(comodel_name='coffee.shop')
    date_from = fields.Date(default=lambda self: fields.Date.today(),
        required=True)
    date_to = fields.Date(default=lambda self: fields.Date.today(),
        required=True)

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for record in self:
            if record.date_to < record.date_from:
                raise UserError("End date is earlier than start date")

    def action_generate_pdf(self):
        return self.env.ref('coffee_shop'
            '.action_report_consumptions').report_action(self)
    def _get_consumptions(self):
        domain = [
                ('consumption_date', '>=', self.date_from),
                ('consumption_date', '<=', self.date_to),
            ]

        if self.coffee_shop_ids:
            domain.append(('coffee_shop_id', 'in', self.coffee_shop_ids.ids))

        return self.env['consumption'].search(domain, order="coffee_shop_id")


class ParticularReport(models.AbstractModel):
    _name = 'report.coffee_shop.template_consumption'

    def _get_report_values(self, docids, data=None):
        record = self.env['wizard.consumption.report'].browse(docids)

        return {
            'consumptions': record._get_consumptions(),
            'get_today': self.get_today,
        }

    def get_today(self):
        return fields.Datetime.to_string(
            fields.Datetime.context_timestamp(
                self, fields.Datetime.now()))
