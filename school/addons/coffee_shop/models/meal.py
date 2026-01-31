# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Meal(models.Model):
    _name = 'meal'
    _description = 'Meal Information'

    name = fields.Char(string='Meal Name', required=True)
    price = fields.Float(string='Price', required=True, default=10.0)
    coffee_shop_ids = fields.Many2many(comodel_name='coffee.shop', string='Coffee Shops', relation='coffee_shop_meal_rel', 
        column1='meal_id', column2='coffee_shop_id')