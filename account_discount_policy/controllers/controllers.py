# -*- coding: utf-8 -*-
# from odoo import http


# class AccountDiscountPolicy(http.Controller):
#     @http.route('/account_discount_policy/account_discount_policy', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_discount_policy/account_discount_policy/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_discount_policy.listing', {
#             'root': '/account_discount_policy/account_discount_policy',
#             'objects': http.request.env['account_discount_policy.account_discount_policy'].search([]),
#         })

#     @http.route('/account_discount_policy/account_discount_policy/objects/<model("account_discount_policy.account_discount_policy"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_discount_policy.object', {
#             'object': obj
#         })

