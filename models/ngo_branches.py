from odoo import models, fields


class NgoBranches(models.Model):
    _name = "ngo.branches"
    _description = "Branch"

    name = fields.Char(string="Branch Name", required=True)
    address = fields.Text(string="Address")
    city_id = fields.Many2one("res.country.state", string="City")
    