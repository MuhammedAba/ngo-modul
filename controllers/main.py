from odoo.addons.web.controllers.main import ensure_db, Home, SIGN_UP_REQUEST_PARAMS
from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.exceptions import UserError, ValidationError
import re
from odoo.addons.web.controllers.main import Home


class CustomerPortal(CustomerPortal):
    OPTIONAL_BILLING_FIELDS = [
        "zipcode",
        "state_id",
        "vat",
        "company_name",
        "test",
        "volunteer_skills",
    ]

    @http.route(["/my/account"], type="http", auth="user", website=True)
    def account(self, redirect=None, **post):
        values = self._prepare_portal_layout_values()
        partner = request.env.user.partner_id
        values.update(
            {
                "error": {},
                "error_message": [],
            }
        )
        countries = request.env["res.country"].sudo().search([])
        states = request.env["res.country.state"].sudo().search([])
        volunteer_skills = request.env["volunteer.skills"].sudo().search([])
        values.update(
            {
                "partner": partner,
                "countries": countries,
                "states": states,
                "has_check_vat": hasattr(request.env["res.partner"], "check_vat"),
                "redirect": redirect,
                "page_name": "my_details",
                "volunteer_skills": volunteer_skills,
            }
        )

        if post and request.httprequest.method == "POST":
            error, error_message = self.details_form_validate(post)
            values.update({"error": error, "error_message": error_message})
            values.update(post)
            if not error:
                values = {key: post[key] for key in self.MANDATORY_BILLING_FIELDS}
                values.update(
                    {
                        key: post[key]
                        for key in self.OPTIONAL_BILLING_FIELDS
                        if key in post
                    }
                )
                for field in set(["country_id", "state_id"]) & set(values.keys()):
                    try:
                        values[field] = int(values[field])
                    except:
                        values[field] = False
                values.update({"zip": values.pop("zipcode", "")})
                partner.sudo().write(values)
                if redirect:
                    return request.redirect(redirect)
                return request.redirect("/my/home")
        response = request.render("portal.portal_my_details", values)
        response.headers["X-Frame-Options"] = "DENY"
        return response


class AuthSignupHome(Home):
    def _prepare_signup_values(self, qcontext):
        values = {key: qcontext.get(key) for key in ("login", "name", "password")}
        email = values.get("login")
        name = values.get("name")

        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        if re.fullmatch(regex, email):
            pass
        else:
            raise ValidationError("Email yapısı uygun değil.")

        if (
            len(name) > 30
            or len(name) < 2
            or any(char in "0123456789_*/+-" for char in name)
        ):
            raise UserError(
                "İsim 30 karakterden fazla olamaz, 2 karakterden az olamaz, sayı ve özel karakter içeremez."
            )

        password = values.get("password")
        if (
            len(password) < 8
            or not any(char.isdigit() for char in password)
            or not any(char in "_*/!$-" for char in password)
        ):
            raise UserError(
                "Şifre en az 8 karakterden oluşmalı ve en az bir sayı ile bir özel karakter (_*/!$-) içermelidir. Lütfen Tekrar girin."
            )
        if values.get("password") != qcontext.get("confirm_password"):
            raise UserError (
                "Şifre eşleşmesi doğrulanmadı tekrar giriniz."
            )

        return values

from odoo import http


class WebsiteForm(http.Controller):

    @http.route("/get_states", type="json", auth="public")
    def get_states(self, country_id):
        states = request.env["res.country.state"].search(
            [("country_id", "=", country_id)]
        )
        return [{"id": state.id, "name": state.name} for state in states]

    @http.route("/get_branches", type="json", auth="public")
    def get_branches(self, state_id):
        branches = request.env["res.city"].search(
            [("state_id", "=", state_id)]
        )
        return [{"id": branch.id, "name": branch.name} for branch in branches]

    @http.route("/subeler", type="http", auth="public", website=True)
    def form_page(self, **kwargs):
        return http.request.render("ngo-modul.website_form_page")

    @http.route("/get_branch_info", type="json", auth="public")
    def get_branch_info(self, branch_id):
        branch = request.env["res.city"].browse(int(branch_id))
        if branch.exists():
            return http.request.env["ir.ui.view"]._render_template(
                "ngo-modul.branch_info",
                {
                    "branch": branch,
                },
            )
        else:
            return {"error": "Branch not found"}
