# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coffee_shop_id = fields.Many2one(comodel_name='coffee.shop', string='Coffee Shop')
    consumption_id = fields.Many2one(comodel_name='consumption', string='Consumption')

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    meal_id = fields.Many2one(comodel_name='meal', string='Meal')
