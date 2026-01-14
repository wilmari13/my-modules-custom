# -*- coding: utf-8 -*-
# from odoo import http


# class BinauralPayrollBenefits(http.Controller):
#     @http.route('/binaural_payroll_benefits/binaural_payroll_benefits', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/binaural_payroll_benefits/binaural_payroll_benefits/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('binaural_payroll_benefits.listing', {
#             'root': '/binaural_payroll_benefits/binaural_payroll_benefits',
#             'objects': http.request.env['binaural_payroll_benefits.binaural_payroll_benefits'].search([]),
#         })

#     @http.route('/binaural_payroll_benefits/binaural_payroll_benefits/objects/<model("binaural_payroll_benefits.binaural_payroll_benefits"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('binaural_payroll_benefits.object', {
#             'object': obj
#         })

