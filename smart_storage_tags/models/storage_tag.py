from odoo import models, fields

class StorageTag(models.Model):
    _name = 'stock.storage.tag'
    _description = 'Etiquetas de Almacenamiento'

    name = fields.Char(string='Nombre', required=True)
    color = fields.Integer(string='Índice de Color')
    description = fields.Text(string='Descripción')