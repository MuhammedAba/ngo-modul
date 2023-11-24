# -*- coding: utf-8 -*-

from odoo import models, fields, api


class VolunteerSkills(models.Model):
    _name = "volunteer.skills"

    name = fields.Char(string="Gönülllü Yetenek İsmi")
    code = fields.Char(string="Kod")
    internal_notes = fields.Text(string="Hakkında")
