# -*- coding: utf-8 -*-
# from odoo import http


# class BinauralStockAlerts(http.Controller):
#     @http.route('/binaural_stock_alerts/binaural_stock_alerts', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/binaural_stock_alerts/binaural_stock_alerts/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('binaural_stock_alerts.listing', {
#             'root': '/binaural_stock_alerts/binaural_stock_alerts',
#             'objects': http.request.env['binaural_stock_alerts.binaural_stock_alerts'].search([]),
#         })

#     @http.route('/binaural_stock_alerts/binaural_stock_alerts/objects/<model("binaural_stock_alerts.binaural_stock_alerts"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('binaural_stock_alerts.object', {
#             'object': obj
#         })

