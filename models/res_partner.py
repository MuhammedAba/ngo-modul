from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partner(models.Model):  # orjinalini yaz
    _description = "Contact"
    _inherit = "res.partner"

    # member_type = fields.Selection(
    #     [("is_volunteer", "Gönüllü"), ("is_donor", "Bağışçı")],
    #     string="Member Type",
    # )
    #volunteer_type = fields.Many2one("volunteer.types", string="Gönüllü Tipi")
    #donor_type = fields.Many2one("donor.types", string="Bağış Türü")
    
    volunteer_skills = fields.Many2many(
        "volunteer.skills", string="Gönüllü Yetenekleri",  widget='many2many_tags'
    )
    test = fields.Char("Test")

    @api.constrains("name")
    def _check_name_length(self):
        for record in self:
            if len(record.name) > 50:
                raise ValidationError("Name cannot be longer than 50 characters.")

    # @api.constrains("phone")
    # def _check_phone_length(self):
    #     for record in (self):
    #         if len(record.phone)> 10:
    #             raise ValidationError("Telefon numarası 10 haneli olmalı!!")