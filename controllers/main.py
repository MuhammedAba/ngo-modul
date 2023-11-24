from odoo import http
from odoo.http import request


# class MyWebsiteController(http.Controller):

#     @http.route('/web/signup?', type='http', auth="user", website=True)
#     def your_route(self, **post):

#         # Telefon bilgisini al
#         phone = post.get('phone')

#         # Telefon bilgisini kaydet
#         if phone:
#             res_partner.write({'phone': phone})
#         return http.request.render('your_module.your_template', {})



class WebsiteController(http.Controller):

    @http.route('/web/signup?', type='http', auth="public", website=True)
    def your_route(self, **kw):
        volunteer_skills = request.env['ngo-modul'].search([]).mapped('volunteer_skills')
        return http.request.render('ngo-modul.res_partner', {'volunteer_skills': volunteer_skills})

















# class StkPage(http.Controller):
#     @http.route("/volunteer_webform", type="http", auth="public", website=True)
#     def volunteer_webform(self, **kw):
#         volSkill_rec = request.env["volunteer.skills"].sudo().search([])
#         return http.request.render(
#             "odoo-ngo.create_member", {'volSkill_rec': volSkill_rec}
#         )

#     @http.route("/create/volunteer", type="http", auth="public", website=True)
#     def create_volunteer(self, **kw):
#         print("Data received...", kw)
#         request.env["res.partner"].sudo().create(kw)
#         return request.render("odoo-ngo.volunteer_thanks", {})
