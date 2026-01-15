from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestInvoiceDiscount(TransactionCase):

    def setUp(self):
        super(TestInvoiceDiscount, self).setUp()
        
        # 1. Creamos las categorías (etiquetas)
        self.cat_vip = self.env['res.partner.category'].create({'name': 'VIP'})
        self.cat_regular = self.env['res.partner.category'].create({'name': 'Regular'})
        
        # 2. Creamos la política de descuento para VIP
        self.policy_vip = self.env['account.discount.policy'].create({
            'name': 'Descuento VIP',
            'discount_percentage': 15.0,
            'category_id': self.cat_vip.id
        })
        
        # 3. Creamos los partners
        self.partner_vip = self.env['res.partner'].create({
            'name': 'Empresa VIP',
            'category_id': [(4, self.cat_vip.id)]
        })
        
        self.partner_normal = self.env['res.partner'].create({
            'name': 'Empresa Normal',
            'category_id': [(4, self.cat_regular.id)]
        })

        # 4. Producto para las líneas de factura
        self.product = self.env['product.product'].create({
            'name': 'Servicio Test',
            'lst_price': 100.0,
            'property_account_income_id': self.env['account.account'].search([('account_type', '=', 'income')], limit=1).id
        })

    def test_invoice_discount_flow(self):
        """Prueba el ciclo completo: asignar, cambiar y limpiar descuento"""
        
        # ESCENARIO 1: Crear factura para VIP
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_vip.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })]
        })
        
        # Forzamos el onchange
        invoice._onchange_partner_recompute_discount()
        
        self.assertEqual(invoice.invoice_line_ids[0].discount, 15.0, "El descuento debería ser 15% para el cliente VIP")

        # ESCENARIO 2: Cambio de Partner a uno sin política (Reset a 0)
        invoice.partner_id = self.partner_normal
        invoice._onchange_partner_recompute_discount()
        
        self.assertEqual(invoice.invoice_line_ids[0].discount, 0.0, "El descuento debería volver a 0 al cambiar a un partner sin política")

    def test_edge_case_multiple_categories(self):
        """Caso límite: Partner con dos categorías, una con descuento y otra no"""
        # Añadimos la categoría VIP al partner normal
        self.partner_normal.write({'category_id': [(4, self.cat_vip.id)]})
        
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_normal.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })]
        })
        
        invoice._onchange_partner_recompute_discount()
        
        # Debería encontrar la política de la categoría VIP aunque tenga otras categorías
        self.assertEqual(invoice.invoice_line_ids[0].discount, 15.0, "Debe aplicar el descuento si al menos una categoría tiene política")