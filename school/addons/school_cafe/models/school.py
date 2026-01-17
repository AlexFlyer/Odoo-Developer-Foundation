# -*- coding: utf-8 -*-
# autor : Isaac Villaseñor
# email: isaac.villasenor@gmail.com
# odoo version 17.0
from odoo import models, fields, api

class School(models.Model):
    _name = 'school.school' 
    _description = 'School Management' 
    _order = 'name asc'

    name = fields.Char(string='School Name', required=True, help='Name of the school', index=True)
    active = fields.Boolean(string='Is Active', default=True, help='Indicates if the school is currently active')
    school_cafeteria_ids = fields.One2many(
        comodel_name='school.cafe',
        inverse_name='school_school_id',
        string='Cafes',
        help='List of cafes associated with this school',
    )
    school_cafe_ids = fields.Many2many(
        comodel_name='school.cafe',
        string='Cafes Many2many',
        help='Many2many relationship with cafes',
    )