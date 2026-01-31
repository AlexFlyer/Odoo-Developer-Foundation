# -*- coding: utf-8 -*-
from odoo import models, fields

class Carrer(models.Model):
    _name = 'coffeshop.carrer'
    _description = 'Carrer'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    student_ids = fields.One2many(comodel_name='coffeshop.student', inverse_name='carrer_id', string='Students')
    consumption_ids = fields.One2many(comodel_name='coffeshop.consumption', inverse_name='carrer_id', string='Consumptions')
    active = fields.Boolean(default=True)
