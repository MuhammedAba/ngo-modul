import http
from urllib import request
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Partner(models.Model):  # orjinalini yaz
    _description = "Contact"
    _inherit = "res.users"
