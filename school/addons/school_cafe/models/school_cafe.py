# -*- coding: utf-8 -*-
# autor : Isaac Villaseñor
# email: isaac.villasenor@gmail.com
# odoo version 17.0
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class SchoolCafe(models.Model):
    _name = 'school.cafe' # el model name es el nombre dee la tabla en la base de datos school_cafe
    _description = 'School Cafe Management' 

    name = fields.Char(string='Cafe Name', required=True, help='en este campo va el nombre de la cafeteria', index=True)
    description = fields.Text(string='Description')
    table_number = fields.Integer(string='Table Number', help='Numero de mesa asignada')
    minimum_order_amount = fields.Float(string='Minimum Order Amount', default=50.0, help='Monto minimo de pedido para la cafeteria')
    active = fields.Boolean(string='Active', default=True)
    launch_date = fields.Date(string='Launch Date', default=fields.Date.today, help='Fecha de lanzamiento de la cafeteria')
    launch_datetime = fields.Datetime(string='Launch DateTime', default=fields.Datetime.now, help='Fecha y hora de lanzamiento de la cafeteria')
    sequence = fields.Integer(string='Sequence', default=10, help='Secuencia para ordenar las cafeterias')

    school_school_id = fields.Many2one(
        comodel_name='school.school',
        string='School',
        ondelete='set null',
        help='The school associated with this cafe',
    )
    discount_rate = fields.Float(string='Discount Rate', default=5.0, help='Discount rate applicable at the cafe')
    minimum_order_amount_with_discount = fields.Float(
        string='Minimum Order Amount with Discount',
        compute='_compute_minimum_order_amount_with_discount',
        store=True,
        help='Minimum order amount after applying discount',
    )
    school_name = fields.Char(related='school_school_id.name', store=True, string='School Name', readonly=True) 
    state = fields.Selection(
        string='State',
        selection=[
            ('open', 'Open'),
            ('closed', 'Closed'),
            ('renovation', 'Under Renovation'),
        ],
        default='open',
        help='Current state of the cafe',
    )

    _sql_constraints = [
        ('unique_name', 'unique(name)', 'Cafe name must be unique.'),
    ]

    @api.onchange('name')
    def _onchange_name(self):
        for record in self:
            if record.name:
                record.name = record.name.upper()

    @api.constrains('minimum_order_amount')
    def _check_minimum_order_amount(self):
        for record in self:
            if record.minimum_order_amount < 0:
                raise ValidationError('Minimum Order Amount cannot be negative.')

    @api.depends('discount_rate','minimum_order_amount')
    def _compute_minimum_order_amount_with_discount(self):
        for record in self:
            if record.discount_rate:
                record.minimum_order_amount_with_discount = record.minimum_order_amount * (1 - record.discount_rate / 100)
            else:
                record.minimum_order_amount_with_discount = record.minimum_order_amount
    
    def action_close_cafe(self):
        for record in self:
            record.state = 'closed'
            if self.env.context.get('table_number'):
                record.table_number = self.env.context['table_number']
            else:
                record.table_number = 0
            record.name = record.name + ' - CLOSED'

    def action_open_cafe(self):
        for record in self:
            record.state = 'open'
            record.name = record.name.replace(' - CLOSED', '')
            record.table_number = 1  # Assign a default table number when opening


    # inherit create method to add pdb for debugging
    @api.model
    def create(self, vals):
        #ctx = self.env.context or {}
        
        #if ctx.get('params')['model'] == 'school.cafe':
        #    vals['description'] = 'Created from school cafe model context'
        #self = self.with_context(default_description='Created via overridden create method')
        # ejemplo de como obtener el name de la escuela relacionada
        #school_id = self.env['school.school'].browse(vals.get('school_school_id')).ensure_one()
        #vals['school_name'] = school_id.name

        #ejemplo de como usar domain to search for related records
        return super(SchoolCafe, self).create(vals)
    
    