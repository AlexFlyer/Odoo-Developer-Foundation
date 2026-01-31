# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'coffeshop.student'
    _description = 'Student'

    sequence = fields.Integer(string='Sequence', default=10)
    name = fields.Char(string='Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    code = fields.Char(string='Student Code')
    carrer_id = fields.Many2one(comodel_name='coffeshop.carrer', string='Carrer')
    active = fields.Boolean(default=True)
    birth_date = fields.Date(string='Birth Date')
    age = fields.Integer(string='Age', compute='_compute_age')
    consumption_ids = fields.One2many(comodel_name='coffeshop.consumption', inverse_name='student_id', string='Consumptions')
    consumption_count = fields.Integer(string='Consumption Count', compute='_compute_consumption_count')
    
    @api.depends('consumption_ids')
    def _compute_consumption_count(self):
        for record in self:
            record.consumption_count = len(record.consumption_ids)

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
                record.age = age
            else:
                record.age = 0
    
    def _compute_display_name(self):
        for record in self:
            record.display_name = "{} {} {}".format(record.name or '', record.middle_name or '', record.last_name or '').strip().upper()

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.age < 18:
                raise ValidationError(_('Student must be at least 18 years old.'))
    
    def action_view_consumptions(self):
        return {
            'name': _('Consumptions'),
            'type': 'ir.actions.act_window',
            'res_model': 'coffeshop.consumption',
            'view_mode': 'tree,form',
            'domain': [('student_id', '=', self.id)],
            'context': {'default_student_id': self.id},
        }
