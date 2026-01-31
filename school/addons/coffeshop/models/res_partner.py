# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    student_id = fields.Many2one(comodel_name='coffeshop.student', string='Student')
