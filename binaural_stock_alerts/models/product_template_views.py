
from odoo import models, fields, api

class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'mail.thread']

    # Campo solicitado: umbral de stock mínimo 
    x_min_stock = fields.Float(string="Stock Mínimo Crítico", default=0.0)

    def check_critical_stock(self):
        """Acción automática para validar stock y generar notificaciones [cite: 48]"""
        for product in self:
            if product.qty_available < product.x_min_stock:
                # Evitar duplicados: Solo notificar si no hay un mensaje reciente similar 
                last_message = self.env['mail.message'].search([
                    ('res_id', '=', product.id),
                    ('model', '=', 'product.template'),
                    ('body', 'like', 'Alerta: Stock Crítico'),
                ], limit=1)
                
                if not last_message:
                    product.message_post(
                        body=f"El Stock esta por debajo del mínimo de ({product.x_min_stock}) unidades, se disponen ({product.qty_available}) unidades.",
                        subtype_xmlid="mail.mt_note"
                    )