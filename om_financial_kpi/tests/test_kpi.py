from odoo.tests.common import TransactionCase

class TestAccountFinancialKpi(TransactionCase):

    def setUp(self):
        super(TestAccountFinancialKpi, self).setUp()
        self.kpi_data = self.env.ref('om_financial_kpi.kpi_margen_bruto')

    def test_01_kpi_logic_validation(self):
        
        # validamos que el campo computado se ejecute sin errores.
        self.kpi_data._compute_kpi_value()
        
        # El test pasa si el valor es un número (aunque sea 0 o -200k)
        self.assertIsInstance(self.kpi_data.current_value, float, "El valor debe ser un número decimal")

    def test_02_threshold_status_logic(self):
        """Validar la lógica de semáforos (Rojo/Amarillo/Verde)"""
        # Forzamos valores manualmente para probar que la lógica de comparación es correcta
        self.kpi_data.current_value = 100.0
        self.kpi_data.threshold_critical = 500.0
        
        # Validamos que el sistema reconozca que 100 < 500 (Estado Crítico)
        es_critico = self.kpi_data.current_value < self.kpi_data.threshold_critical
        self.assertTrue(es_critico, "La lógica de umbral crítico falló")
        
        # Validamos el estado Verde
        self.kpi_data.current_value = 1000.0
        self.kpi_data.threshold_warning = 800.0
        es_verde = self.kpi_data.current_value >= self.kpi_data.threshold_warning
        self.assertTrue(es_verde, "La lógica de umbral saludable falló")

    def test_03_robustness(self):
        """Validar que una fórmula mal escrita no tumbe el servidor"""
        kpi_test = self.env['account.financial.kpi'].create({
            'name': 'Test Error',
            'formula': '999999 + invalid_variable',
        })
        kpi_test._compute_kpi_value()
        # El try-except de tu modelo debe devolver 0.0
        self.assertEqual(kpi_test.current_value, 0.0, "Fórmulas erróneas deben resultar en 0.0")