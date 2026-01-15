from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    # Relacionamos al cliente directamente con una política de descuento
    discount_policy_id = fields.Many2one(
        'account.discount.policy', 
        string='Política de Descuento Predeterminada'
    )


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.onchange('invoice_line_ids', 'partner_id')
    def _onchange_discount_policy_id(self):
        # 1. Verificamos que haya un partner y que ese partner tenga política
        if self.partner_id and self.partner_id.discount_policy_id:
            policy_discount = self.partner_id.discount_policy_id.discount_percentage
            
            for line in self.invoice_line_ids:
                # 2. Solo aplicamos si el descuento es diferente para evitar bucles 
                if line.display_type not in ('line_section', 'line_note'):
                    if line.discount != policy_discount:
                        line.discount = policy_discount
        
        # Si el partner NO tiene política, resetear a 0:
        elif self.partner_id and not self.partner_id.discount_policy_id:
            for line in self.invoice_line_ids:
                line.discount = 0.0

                    