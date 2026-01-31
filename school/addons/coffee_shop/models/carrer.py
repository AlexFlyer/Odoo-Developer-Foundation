# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Carrer(models.Model):
    _name = 'carrer'
    _description = 'Carrer'

    name = fields.Char(string='Carrer Name', required=True)
    student_ids = fields.One2many(comodel_name='student', inverse_name='carrer_id', string='Students')
    