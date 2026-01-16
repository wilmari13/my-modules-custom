from odoo import models, fields, api

class ManageStorageTagsWizard(models.TransientModel):
    _name = 'manage.storage.tags.wizard'
    _description = 'Gestionar Etiquetas de Almacenamiento'

    product_tmpl_id = fields.Many2one('product.template', string='Producto', required=True)
    tag_ids = fields.Many2many('stock.storage.tag', string='Etiquetas')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Obtenemos el ID del producto desde el contexto del Kanban
        active_id = self.env.context.get('active_id')
        if active_id:
            product = self.env['product.template'].browse(active_id)
            res.update({
                'product_tmpl_id': active_id,
                'tag_ids': [(6, 0, product.storage_tag_ids.ids)]
            })
        return res

    def action_apply(self):
        # Aplicamos los cambios al producto original
        self.product_tmpl_id.storage_tag_ids = [(6, 0, self.tag_ids.ids)]
        return {'type': 'ir.actions.client', 'tag': 'reload'}