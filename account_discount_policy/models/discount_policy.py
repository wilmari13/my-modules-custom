from odoo import models, fields

class DiscountPolicy(models.Model):
    _name = 'account.discount.policy'
    _description = 'Política de Descuento Configurable'

    name = fields.Char(string='Nombre de la Política', required=True)
    discount_percentage = fields.Float(string='Descuento (%)', default=0.0)
    