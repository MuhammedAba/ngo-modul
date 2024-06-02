import http
from urllib import request
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import re


class City(models.Model):  # orjinalini yaz
    _description = "City"
    _inherit = "res.city"

    branch_baskan=fields.Char(string="Şube Başkanı")
    branch_address=fields.Text(string="Şube Adresi")
    branch_phone=fields.Char(string="Telefon No")
    branch_fax=fields.Char(string="Fax") 