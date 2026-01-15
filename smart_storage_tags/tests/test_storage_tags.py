from odoo.tests.common import TransactionCase

class TestStorageTags(TransactionCase):
    def setUp(self):
        super(TestStorageTags, self).setUp()
        self.tag = self.env['stock.storage.tag'].create({
            'name': 'Inflamable',
            'color': 2
        })
        self.product = self.env['product.template'].create({
            'name': 'Alcohol Isopropílico',
            'type': 'consu'
        })

    def test_tag_assignment(self):
        """Valida la asignación de etiquetas a productos"""
        self.product.storage_tag_ids = [(4, self.tag.id)]
        self.assertIn(self.tag, self.product.storage_tag_ids, "La etiqueta no se asignó correctamente.")

        # Buscamos productos que tengan esta etiqueta
        found = self.env['product.template'].search([('storage_tag_ids', 'in', self.tag.id)])
        self.assertIn(self.product, found, "El producto no aparece bajo la etiqueta en el Kanban.")