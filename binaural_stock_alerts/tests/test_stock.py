from odoo.tests.common import TransactionCase
from odoo.fields import Command

class TestStockAlert(TransactionCase):

    def setUp(self):
        """Configuración inicial para las pruebas"""
        super(TestStockAlert, self).setUp()
        # Creamos un producto de prueba con un stock mínimo de 10
        self.product = self.env['product.template'].create({
            'name': 'Producto de Prueba',
            'type': 'product',
            'x_min_stock': 10.0,
        })

    def test_01_stock_low_notification(self):
        """Validar que se genera notificación cuando el stock es bajo"""
        # Simulamos que el stock disponible es 5 (menor al umbral de 10)
        # Nota: En pruebas, qty_available puede requerir manipular stock.quant
        # Aquí forzamos la ejecución de la lógica del método
        self.product.check_critical_stock()

        # Buscamos si existe el mensaje en el chatter del producto
        message = self.env['mail.message'].search([
            ('res_id', '=', self.product.id),
            ('model', '=', 'product.template'),
            ('body', 'like', 'Alerta: Stock Crítico')
        ])
        
        self.assertTrue(message, "Debería haberse generado un mensaje de alerta.")

    def test_02_no_duplicate_notifications(self):
        """Validar que no se generen duplicados innecesarios""" 
        # Ejecutamos dos veces
        self.product.check_critical_stock()
        self.product.check_critical_stock()

        messages = self.env['mail.message'].search([
            ('res_id', '=', self.product.id),
            ('model', '=', 'product.template'),
            ('body', 'like', 'Alerta: Stock Crítico')
        ])
        
        self.assertEqual(len(messages), 1, "No deberían existir mensajes duplicados.")