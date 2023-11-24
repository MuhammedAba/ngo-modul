# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProjectSkills(models.Model):
    _name = "project.skills"

    name = fields.Char(string="Proje Yetenek İsmi")
    code = fields.Char(string="Kod")
    internal_notes = fields.Text(string="Hakkında")