# -*- coding: utf-8 -*-
# autor : Isaac Villaseñor
# email: isaac.villasenor@gmail.com
# odoo version 17.0
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_cafe_supplier = fields.Boolean(string='Is Cafe Supplier', default=False, help='Indicates if the partner is a cafe supplier')

    cafe_supplier_code = fields.Char(string='Cafe Supplier Code', help='Unique code for the cafe supplier')

    @api.constrains('cafe_supplier_code')
    def _check_cafe_supplier_code(self):
        for record in self:
            if record.is_cafe_supplier and not record.cafe_supplier_code:
                raise ValidationError('Cafe Supplier Code must be set for cafe suppliers.')
