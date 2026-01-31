# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CoffeeShop(models.Model):
    _name = 'coffee.shop'
    _description = 'Coffee Shop Information'

    name = fields.Char(string='Coffee Shop Name', required=True)
    location = fields.Char(string='Location')
    meal_ids = fields.Many2many(comodel_name='meal', string='Meals', relation='coffee_shop_meal_rel', 
        column1='coffee_shop_id', column2='meal_id')