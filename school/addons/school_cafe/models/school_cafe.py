# -*- coding: utf-8 -*-
# autor : Isaac Villaseñor
# email: isaac.villasenor@gmail.com
# odoo version 17.0
from odoo import models, fields, api

class SchoolCafe(models.Model):
    _name = 'school.cafe' # el model name es el nombre dee la tabla en la base de datos school_cafe
    _description = 'School Cafe Management' 

    name = fields.Char(string='Cafe Name', required=True)
    description = fields.Text(string='Description')

    # inherit create method to add pdb for debugging
    @api.model
    def create(self, vals):
        import pdb; pdb.set_trace()
        return super(SchoolCafe, self).create(vals)
    
    