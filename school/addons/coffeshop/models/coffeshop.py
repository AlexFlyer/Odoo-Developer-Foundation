# -*- coding: utf-8 -*-
from odoo import models, fields

class Coffeshop(models.Model):
    _name = 'coffeshop.coffeshop'
    _description = 'Coffeshop'

    name = fields.Char(string='Name', required=True)
    location = fields.Char(string='Location')
    active = fields.Boolean(default=True)
    meal_ids = fields.Many2many(comodel_name='coffeshop.meal', string='Meals Available', 
            relation='coffeshop_meal_rel', column1='coffeshop_id', column2='meal_id')    
