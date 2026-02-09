from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('partner_id', 'invoice_line_ids')
    def _onchange_partner_recompute_discount(self):
        
        new_discount = 0.0
        if self.partner_id:
            #buscamos si hay categoria asociada
            policy = self.env['account.discount.policy'].search([
                ('category_id', 'in', self.partner_id.category_id.ids)
            ], order='discount_percentage desc', limit=1)
            
            if policy:
                new_discount = policy.discount_percentage

        # 2. Aplicar el descuento (o 0.0) a todas las líneas
        for line in self.invoice_line_ids:
            if line.display_type not in ('line_section', 'line_note'):
                line.discount = new_discount