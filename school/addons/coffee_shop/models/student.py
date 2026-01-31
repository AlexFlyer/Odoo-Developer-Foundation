# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Student(models.Model):
    _name = 'student'
    _description = 'Student Information'

    name = fields.Char(string='Name', required=True)
    middle_name = fields.Char(string='Middle Name')
    last_name = fields.Char(string='Last Name')
    sequence = fields.Integer(string='Sequence', default=10)
    carrer_id = fields.Many2one(comodel_name='carrer', string='Carrer')
    consumptions_ids = fields.One2many(comodel_name='consumption', inverse_name='student_id', string='Consumptions')
    count_consumptions = fields.Integer(string='Number of Consumptions', compute='_compute_count_consumptions')
    birth_date = fields.Date(string='Birth Date', required=True)
    age = fields.Integer(string='Age', compute='_compute_age')

    @api.depends('consumptions_ids')
    def _compute_count_consumptions(self):
        for record in self:
            record.count_consumptions = len(record.consumptions_ids)    

    def _compute_display_name(self):
        for record in self:
            record.display_name = "{} {} {}".format(record.name or '', record.middle_name or '', record.last_name or '').strip()

    @api.depends('birth_date')
    def _compute_age(self):
        for record in self:
            if record.birth_date:
                today = fields.Date.today()
                age = today.year - record.birth_date.year - ((today.month, today.day) < (record.birth_date.month, record.birth_date.day))
                record.age = age
            else:
                record.age = 0

    @api.constrains('birth_date')
    def _check_birth_date(self):
        for record in self:
            if record.age <= 18:
                raise ValidationError("Student must be at least 18 years old.")
            
    def action_view_consumptions(self):
        self.ensure_one()
        action = {
            'name': _('Consumption %s') % (self.display_name,),
            'type': 'ir.actions.act_window',
            'res_model': 'consumption',
            'context': {'default_student_id': self.id, 'default_state': 'draft'},
        }

        if len(self.consumptions_ids) > 1:
            action.update({
                'view_mode': 'tree,form',
                'domain': [('student_id', '=', self.id)],
            })
        else:
            action.update({
                'view_mode': 'form',
                'res_id': self.consumptions_ids.id or False,
            })
        return action