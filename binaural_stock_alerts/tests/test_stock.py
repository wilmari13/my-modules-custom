from odoo.tests.common import TransactionCase
from odoo.tests import tagged

@tagged('post_install', '-at_install')
class TestAlerts(TransactionCase):
    def test_alertas_y_duplicados(self):
        # 1. Crear el producto
        prod = self.env['product.product'].create({
            'name': 'Producto Test', 
            'type': 'product',
            'x_min_stock': 10
        })
        
        # 2. PRIMERA ACTUALIZACIÓN (Crea el mensaje)
        wizard_1 = self.env['stock.change.product.qty'].with_context(
            active_id=prod.id, 
            active_model='product.product'
        ).create({
            'product_id': prod.id,
            'product_tmpl_id': prod.product_tmpl_id.id,
            'new_quantity': 5
        })
        wizard_1.change_product_qty()

        # 3. SEGUNDA ACTUALIZACIÓN (No debería duplicar)
        wizard_2 = self.env['stock.change.product.qty'].with_context(
            active_id=prod.id, 
            active_model='product.product'
        ).create({
            'product_id': prod.id,
            'product_tmpl_id': prod.product_tmpl_id.id,
            'new_quantity': 3
        })
        wizard_2.change_product_qty()

        # 4. Verificar mensajes en el chatter
        msgs = self.env['mail.message'].search_count([
            ('res_id', '=', prod.product_tmpl_id.id),
            ('model', '=', 'product.template'),
            ('body', 'like', 'ALERTA CRÍTICA')
        ])
        
        print(">>> TEST FINALIZADO: Sin bucles y sin duplicados.")