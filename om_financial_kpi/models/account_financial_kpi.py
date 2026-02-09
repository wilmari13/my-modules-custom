from odoo import models, fields, api
from odoo.tools.safe_eval import safe_eval

class AccountFinancialKpi(models.Model):
    _name = 'account.financial.kpi'
    _description = 'KPI Financiero'

    name = fields.Char(string="Nombre del KPI", required=True)
    formula = fields.Char(
        string="Fórmula", 
        help="Use códigos de cuentas. Ej: 101100 + 101200",
        required=True
    )
    threshold_warning = fields.Float(string="Umbral Amarillo", default=0.0)
    threshold_critical = fields.Float(string="Umbral Rojo", default=0.0)
    current_value = fields.Float(compute="_compute_kpi_value", string="Valor Actual")

    @api.depends('formula')
    def _compute_kpi_value(self):
        # 1. Buscamos todas las cuentas
        accounts = self.env['account.account'].search([])
        
        # 2. Creamos el diccionario. 
                
        context_dict = {}
        for acc in accounts:
            # Usamos acc.code como clave y el saldo actual como valor
            context_dict[acc.code] = acc.current_balance or 0.0
            
        for record in self:
            if not record.formula:
                record.current_value = 0.0
                continue
                
            try:
                # 3. Limpiamos la fórmula por si hay espacios raros
                clean_formula = record.formula.replace(' ', '')
                
                # Evaluamos
                result = safe_eval(clean_formula, {}, context_dict)
                record.current_value = float(result)
            except Exception:
                record.current_value = 0.0