from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestDiscountPolicy(TransactionCase):

    def setUp(self):
        super(TestDiscountPolicy, self).setUp()
        # 1. Crear una política de descuento del 15%
        self.policy_15 = self.env['account.discount.policy'].create({
            'name': 'Descuento VIP 15',
            'discount_percentage': 15.0,
        })

        # 2. Crear un cliente y asignarle la política
        self.partner_vip = self.env['res.partner'].create({
            'name': 'Cliente de Prueba VIP',
            'discount_policy_id': self.policy_15.id,
        })

        # 3. Crear un producto para la factura
        self.product = self.env['product.product'].create({
            'name': 'Producto de Prueba',
            'lst_price': 100.0,
        })

    def test_automatic_discount_application(self):
        """Verificar que el descuento se aplique al disparar el onchange"""
        # Crear una factura en borrador
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.partner_vip.id,
            'invoice_line_ids': [(0, 0, {
                'product_id': self.product.id,
                'quantity': 1,
                'price_unit': 100.0,
            })]
        })

        # Simular el disparo del onchange de las líneas de factura
        invoice._onchange_discount_policy_id()

        # Verificar que el descuento de la línea sea igual al de la política del partner
        self.assertEqual(
            invoice.invoice_line_ids[0].discount, 
            15.0, 
            "El descuento debería ser del 15% según la política del cliente"
        )