# -*- coding: utf-8 -*-
from odoo import models, fields

class Meal(models.Model):
    _name = 'coffeshop.meal'
    _description = 'Meal'

    name = fields.Char(string='Name', required=True)
    price = fields.Float(string='Price')
    active = fields.Boolean(default=True)
    coffeshop_ids = fields.Many2many(comodel_name='coffeshop.coffeshop', string='Coffeshops Offering This Meal',
            relation='coffeshop_meal_rel', column1='meal_id', column2='coffeshop_id')
