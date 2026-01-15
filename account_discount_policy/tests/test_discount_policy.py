from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError

class TestInvoiceDiscount(TransactionCase):

    def setUp(self):
        super(TestInvoiceDiscount, self).setUp()
        # 1. Crear una política de descuento 
        self.policy_10 = self.env['account.discount.policy'].create({
            'name': 'Descuento 10%',
            'discount_percentage': 10.0
        })
        
        # 2. Cliente con descuento
        self.partner_with_discount = self.env['res.partner'].create({
            'name': 'Cliente VIP',
            'discount_policy_id': self.policy_10.id
        })
        
        # 3. Cliente sin descuento
        self.partner_no_discount = self.env['res.partner'].create({
            'name': 'Cliente Normal',
            'discount_policy_id': False
        })

        # 4. Producto de prueba
        self.product = self.env['product.product'].create({
            'name': 'Producto Test',
            'lst_price': 100.0
        })

    def test_01_invoice_with_discount(self):
        """Validar factura con descuento aplicado automáticamente"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_with_discount.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
                'tax_ids': [(5, 0, 0)],
            })]
        })
        # Forzar el onchange
        invoice._onchange_discount_policy_id()
        
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.discount, 10.0, "El descuento debería ser del 10%")
        self.assertEqual(invoice.amount_total, 90.0, "El total debería reflejar el descuento")

    def test_02_invoice_without_discount(self):
        """Validar factura sin descuento"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_no_discount.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
                'tax_ids': [(5, 0, 0)],
            })]
        })
        invoice._onchange_discount_policy_id()
        
        line = invoice.invoice_line_ids[0]
        self.assertEqual(line.discount, 0.0, "El descuento debería ser 0")
        self.assertEqual(invoice.amount_total, 100.0)

    def test_03_edge_case_zero_price_and_quantity(self):
        """Caso límite: Cantidad o precio cero"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_with_discount.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 0,
                'price_unit': 0,
            })]
        })
        invoice._onchange_discount_policy_id()
        self.assertEqual(invoice.invoice_line_ids[0].discount, 10.0, "Aun con precio 0, el % se debe asignar")

    def test_04_change_partner_update_discount(self):
        """Caso límite: Cambiar el cliente después de agregar líneas"""
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_no_discount.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })]
        })
        # Cambiamos a un cliente con descuento
        invoice.partner_id = self.partner_with_discount
        invoice._onchange_discount_policy_id()
        
        self.assertEqual(invoice.invoice_line_ids[0].discount, 10.0, "El descuento no se actualizó al cambiar el partner")