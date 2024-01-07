import http
from urllib import request
from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re


class Partner(models.Model):  # orjinalini yaz
    _description = "Contact"
    _inherit = "res.partner"

    # member_type = fields.Selection(
    #     [("is_volunteer", "Gönüllü"), ("is_donor", "Bağışçı")],
    #     string="Member Type",
    # )
    # volunteer_type = fields.Many2one("volunteer.types", string="Gönüllü Tipi")
    # donor_type = fields.Many2one("donor.types", string="Bağış Türü")

    volunteer_skills = fields.Many2one("volunteer.skills", string="Gönüllü Yetenekleri")
    test = fields.Char("Test")

    # CHECK FOR NAME
    @api.constrains("name")
    def _check_name(self):
        nums = "1234567890"
        for record in self:
            if len(record.name) > 30:
                print("büyük++++++++++++++++++")
                raise ValidationError(_("Name cannot be longer than 50 characters."))
            elif len(record.name) < 2:
                print("küçük++++++++++++++++++", len(record.name))
                raise ValidationError(_("Name cannot be shorter than 2 characters."))
            for i in record.name:
                for j in nums:
                    if i == j:
                        raise ValidationError(_("Name cannot include numbers."))

    # CHECK FOR EMAIL

    @api.constrains("email")
    def _check_email(self):
        for record in self:
            regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
            if re.fullmatch(regex, record.email):
                pass
            else:
                raise ValidationError(_("Email is not valid"))
