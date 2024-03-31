import http
from urllib import request
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re


class Partner(models.Model):  # orjinalini yaz
    _description = "Contact"
    _inherit = "res.partner"

    # member_type = fields.Selection(
    #     [("is_volunteer", "Gönüllü"), ("is_donor", "Bağışçı")], string="Member Type",
    #     )
    # volunteer_type = fields.Many2one("volunteer.types", string="Gönüllü Tipi")
    # donor_type = fields.Many2one("donor.types", string="Bağış Türü")

    volunteer_skills = fields.Many2one("volunteer.skills", string="Gönüllü Yeteneği")
    #member_types = fields.Many2one("member.types", string="Üye Tipi")
