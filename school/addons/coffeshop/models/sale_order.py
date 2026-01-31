# -*- coding: utf-8 -*-
from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    coffeshop_id = fields.Many2one(comodel_name='coffeshop.coffeshop', string='Coffeshop')
    consumption_id = fields.Many2one(comodel_name='coffeshop.consumption', string='Consumption')


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    meal_id = fields.Many2one(comodel_name='coffeshop.meal', string='Meal')