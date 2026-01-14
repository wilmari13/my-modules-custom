# -*- coding: utf-8 -*-
# from odoo import http


# class SmartStorageTags(http.Controller):
#     @http.route('/smart_storage_tags/smart_storage_tags', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/smart_storage_tags/smart_storage_tags/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('smart_storage_tags.listing', {
#             'root': '/smart_storage_tags/smart_storage_tags',
#             'objects': http.request.env['smart_storage_tags.smart_storage_tags'].search([]),
#         })

#     @http.route('/smart_storage_tags/smart_storage_tags/objects/<model("smart_storage_tags.smart_storage_tags"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('smart_storage_tags.object', {
#             'object': obj
#         })

