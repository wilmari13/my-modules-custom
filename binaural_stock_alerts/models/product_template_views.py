import logging
from odoo import models, fields, api, _
# Configuramos el logger
_logger = logging.getLogger(__name__)
class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'mail.thread']

    # Campo solicitado: umbral de stock mínimo 
    x_min_stock = fields.Float(string="Stock Mínimo Crítico", default=0.0)

    x_is_critical = fields.Boolean(
        string="Estado Crítico", 
        compute="_compute_is_critical", 
        store=True # Importante para poder agrupar en vistas
    )

    @api.depends('qty_available', 'x_min_stock')
    def _compute_is_critical(self):
        for product in self:
            product.x_is_critical = product.qty_available < product.x_min_stock

    
    def _check_min_stock_alert(self):
        """Método reutilizable para validar stock crítico"""
        for template in self:
            if template.x_min_stock > 0 and template.qty_available < template.x_min_stock:
                # Evitar duplicados
                last_message = self.env['mail.message'].search([
                    ('res_id', '=', template.id),
                    ('model', '=', 'product.template'),
                    ('body', 'like', '¡Atención! El stock de'),
                ], limit=1)

                if not last_message:
                    msg = _("¡Atención! El stock de '%s' ha quedado en %s, por debajo del mínimo de %s.") % (
                        template.name, template.qty_available, template.x_min_stock
                    )
                    template.message_post(
                        body=f"⚠️ {msg}",
                        message_type='notification',
                        subtype_xmlid="mail.mt_note",
                        author_id=self.env.ref('base.partner_root').id
                    )

class StockChangeProductQty(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    def change_product_qty(self):
        res = super(StockChangeProductQty, self).change_product_qty()
        for wizard in self:
            # Llamamos al método centralizado
            wizard.product_id.product_tmpl_id._check_min_stock_alert()
        return res



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        res = super(StockPicking, self).button_validate()
        
        # Obtenemos los templates de los productos involucrados
        templates = self.move_ids_without_package.mapped('product_id.product_tmpl_id')
        
        # Llamamos al método centralizado una sola vez por producto
        templates._check_min_stock_alert()
        
        return res