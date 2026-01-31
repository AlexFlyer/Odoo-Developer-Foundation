from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class WizardConsumptionReport(models.TransientModel):
    _name = 'wizard.consumption.report'
    _description = 'Wizard Consumption Report'

    date_from = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_to = fields.Date(string='End Date', required=True, default=fields.Date.today)
    coffeshop_ids = fields.Many2many(comodel_name='coffeshop.coffeshop', string='Coffeshops')

    @api.constrains('date_from', 'date_to')
    def _check_dates(self):
        for record in self:
            if record.date_to < record.date_from:
                raise ValidationError(_('End date cannot be earlier than start date.'))

    def action_generate_pdf(self):
        return self.env.ref('coffeshop.action_report_consumption_pdf').report_action(self)
    
    def _get_consumption(self):
        domain = [
            ('consumption_date', '>=', self.date_from),
            ('consumption_date', '<=', self.date_to),
        ]
        if self.coffeshop_ids:
            domain.append(('coffeshop_id', 'in', self.coffeshop_ids.ids))
        return self.env['coffeshop.consumption'].search(domain)

class ConsuptionReport(models.AbstractModel):
    _name = 'report.coffeshop.report_consumption_pdf'
    _description = 'Consumption Report PDF'

    def _get_report_values(self, docids, data=None):
        wizard = self.env['wizard.consumption.report'].browse(docids)
        
        return {
            'consumptions': wizard._get_consumption(),
        }
    
    def get_today(self):
        return fields.Datetime.to_string(
            fields.Datetime.context_timestamp(
                self, fields.Datetime.now()))
