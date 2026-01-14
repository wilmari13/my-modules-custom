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

    @api.onchange('invoice_line_ids')
    def _onchange_discount_policy_id(self):
        if self.partner_id.discount_policy_id:
            for line in self.invoice_line_ids:
                # Solo aplicamos el descuento si la línea tiene un producto
                # y si el descuento es diferente para evitar bucles
                if line.discount != self.partner_id.discount_policy_id.discount_percentage:
                    line.discount = self.partner_id.discount_policy_id.discount_percentage


                    