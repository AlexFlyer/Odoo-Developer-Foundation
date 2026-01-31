# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Consumption(models.Model):
    _name = 'consumption'
    _description = 'Student Consumption Record'

    name = fields.Char(string='Consumption')
    consumption_date = fields.Date(string='Date', default=fields.Date.today)
    coffee_shop_id = fields.Many2one(comodel_name='coffee.shop', string='Coffee Shop')
    student_id = fields.Many2one(comodel_name='student', string='Student')
    meal_id = fields.Many2one(comodel_name='meal', string='Meal', domain="[('coffee_shop_ids', 'in', coffee_shop_id)]")
    state = fields.Selection(string='State', selection=[('draft', 'Draft'), ('delivered', 'Delivered'), ('cancelled', 'Cancelled')], default='draft')

    _sql_constraints = [
        ('unique_consumption', 'unique(student_id, consumption_date)', 'A student cannot have multiple consumptions on the same date.')
    ]
    
    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_create_sale(self):
        sale_order_obj = self.env['sale.order']
        partner_obj = self.env['res.partner']
        product_consumption_id = self.env.ref('coffee_shop.product_consumption')
        date_order = self.env.context.get('coffee_shop_date_order')
        sales_by_student = {}
        for record in self:
            if record.student_id.id in sales_by_student:
                order_lines = sales_by_student[record.student_id.id]['order_line']

                if record.meal_id.id in order_lines:
                    order_lines[record.meal_id.id]['product_uom_qty'] += 1
                else:
                    order_lines[record.meal_id.id] = {
                            'product_id': product_consumption_id.id,
                            'meal_id': record.meal_id.id,
                            'name': record.meal_id.name,
                            'product_uom_qty': 1,
                            'price_unit': record.meal_id.price,
                        }
            else:
                partner = partner_obj.search(
                    [('student_id', '=', record.student_id.id)], limit=1)

                if not partner:
                    raise ValidationError(_("No client found with student %s", self.student_id.display_name))
                
                sales_by_student[record.student_id.id] = {
                    'date_order': fields.Date.to_string(date_order or record.consumption_date),
                    'partner_id': partner.id,
                    'consumption_id': record.id,
                    'coffee_shop_id': record.coffee_shop_id.id,
                    'order_line': {
                        record.meal_id.id: {
                            'product_id': product_consumption_id.id,
                            'meal_id': record.meal_id.id,
                            'name': record.meal_id.name,
                            'product_uom_qty': 1,
                            'price_unit': record.meal_id.price,
                        }
                    },
                }

        sales = []

        for student_id, sale_data in sales_by_student.items():
            sale_data['order_line'] = [(0, 0, line)
                for meal_id, line in sale_data['order_line'].items()]

            sales.append(sale_data)

        new_sales = sale_order_obj.create(sales)

        self.write({'state': 'delivered'})

        return {
            'type': 'ir.actions.act_window',
            'name': "Sales",
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', new_sales.ids)]
        }
        
    @api.constrains('student_id', 'consumption_date')
    def _check_unique_consumption(self):
        for record in self:
            if self.search_count([
                        ('student_id', '=', record.student_id.id),
                        ('consumption_date', '=', record.consumption_date),
                        ('id', '!=', record.id)
                    ]) > 0:
                raise ValidationError('A student cannot have multiple consumptions on the same date.')
            
    def unlink(self):
        for record in self:
            if record.state == 'delivered':
                raise ValidationError("It can't be deleted once delivered.")
        return super(Consumption, self).unlink()

    @api.model_create_multi
    def create(self, vals_list):
       sequence = self.env.ref('coffee_shop.sequence_consumption')
       for vals in vals_list:
           vals['name'] = sequence.next_by_id()
       return super(Consumption, self).create(vals_list)