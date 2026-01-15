from odoo import models, fields, api, _

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

class StockChangeProductQty(models.TransientModel):
    _inherit = 'stock.change.product.qty'

    def change_product_qty(self):
        """
        Heredo la confirmación del wizard. 
        Muestra alerta si el stock es bajo pero permite que el proceso termine.
        """
        # 1. Ejecutar la lógica original de Odoo (Actualiza el stock)
        res = super(StockChangeProductQty, self).change_product_qty()

        for wizard in self.sudo():
            product = wizard.product_id
            template = product.product_tmpl_id
            
            print(f"=== Procesando Stock para: {product.name} ===")
            print(f"Cantidad actual: {product.qty_available} | Mínimo: {template.x_min_stock}")

            # 2. Validar stock crítico
            if template.x_min_stock > 0 and product.qty_available < template.x_min_stock:
                last_message = self.env['mail.message'].search([
                    ('res_id', '=', product.id),
                    ('model', '=', 'product.template'),
                    ('body', 'like', '¡Atención! El stock de'),
                ], limit=1)

                if not last_message:
                    msg = _("¡Atención! El stock de '%s' ha quedado en %s, por debajo del mínimo de %s.") % (
                        product.name, product.qty_available, template.x_min_stock
                    )

                    template.message_post(
                        body=f"⚠️ {msg}",
                        message_type='notification',
                        subtype_xmlid="mail.mt_note",
                        author_id=self.env.ref('base.partner_root').id # Enviado por OdooBot
                    )
        return res