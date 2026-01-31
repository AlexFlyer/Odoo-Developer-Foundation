# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Consumption(models.Model):
    _name = 'coffeshop.consumption'
    _description = 'Consumption'

    name = fields.Char(string='Name')
    student_id = fields.Many2one(comodel_name='coffeshop.student', string='Student', required=True)
    coffeshop_id = fields.Many2one(comodel_name='coffeshop.coffeshop', string='Coffeshop', required=True)
    meal_id = fields.Many2one(comodel_name='coffeshop.meal', string='Meal', required=True, domain="[('coffeshop_ids', 'in', coffeshop_id)]")
    consumption_date = fields.Date(string='Consumption Date', required=True, default=fields.Date.today)
    active = fields.Boolean(default=True)
    carrer_id = fields.Many2one(comodel_name='coffeshop.carrer', string='Carrer', related='student_id.carrer_id', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], string='State', default='draft')

    _sql_constraints = [
        ('unique_consumption', 'unique(student_id, consumption_date)', 'A student can only have one consumption per day!')
    ]

    @api.constrains('student_id', 'consumption_date')
    def _check_unique_consumption(self):
        for record in self:
            existing = self.search([
                ('student_id', '=', record.student_id.id),
                ('consumption_date', '=', record.consumption_date),
                ('id', '!=', record.id)
            ])
            if existing:
                raise ValidationError(_('A student can only have one consumption per day!'))
    
    @api.onchange('coffeshop_id')
    def _onchange_coffeshop_id(self):
        self.meal_id = False

    @api.model_create_multi
    def create(self, vals_list):
        #sequence = self.env['ir.sequence'].next_by_code('coffeshop.consumption')
        sequence = self.env.ref('coffeshop.sequence_consumption')
        for vals in vals_list:
            vals['name'] = sequence.next_by_id()
        return super().create(vals_list)

    def unlink(self):
        for record in self:
            if record.state == 'delivered':
                raise ValidationError(_('Delivered consumptions cannot be deleted.'))
        return super().unlink()
    
    def action_create_sale_order(self):
        sale_order_obj = self.env['sale.order']
        partner_obj = self.env['res.partner']
        product_consumption = self.env.ref('coffeshop.product_consumption')
    
        sale_ids = []
        for record in self:
            partner_id = partner_obj.search([('student_id', '=', record.student_id.id)], limit=1)
            if not partner_id:
                raise ValidationError(_('No partner associated with the student %s') % (record.student_id.display_name,))
            
            sale_order = sale_order_obj.create({
                'consumption_id': record.id,
                'partner_id': partner_id.id,
                'coffeshop_id': record.coffeshop_id.id,
                'order_line': [(0, 0, {
                    'product_id': product_consumption.id,
                    'product_uom_qty': 1,
                    'price_unit': record.meal_id.price,
                    'meal_id': record.meal_id.id,
                    'name': record.meal_id.name,
                })],

            })
            sale_ids.append(sale_order.id)
            record.state = 'delivered'
        
        return {
            'type': 'ir.actions.act_window',
            'name': "Sales",
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', sale_ids)]
        }
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    