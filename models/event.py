from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EventEvent(models.Model):
    _inherit = "event.event"
    _description = "Event"

    project_skills = fields.Many2many("project.skills", string="Proje Yetenekleri")
    tetiklendi_flag = fields.Boolean(default=True)

    @api.onchange("stage_id")
    def on_change_stage(self):
        partners = self.env["res.partner"].search([])
        kontrol = 0
        gonderiliyor_stage_no = self.env["event.stage"].search(
            args=[("name", "=", "Mail Gönderiliyor")]
        )
        etkinlikler = self.env["event.event"].search(
            args=[("stage_id", "=", gonderiliyor_stage_no.id)]
        )
        gonderildi_stage_no = self.env["event.stage"].search(
            args=[("name", "=", "Mail Gönderildi")]
        )
        gonderilemedi_stage_no = self.env["event.stage"].search(
            args=[("name", "=", "Mail Gönderilemedi")]
        )

        for partner in partners:
            for event in etkinlikler:
                if partner.volunteer_skills.id == event.tag_ids.id:
                    print(
                        "*******************************************"
                        + f"Eşleşen Kayıt - Partner: {partner.name}, Event: {event.name}"
                        + "***************************"
                    )

        print("***********************************: ", len(etkinlikler))
        if len(etkinlikler) > 0:
            for etkinlik in etkinlikler:
                print("Etkinlik no1:", etkinlik.stage_id)
                if kontrol == 1:
                    etkinlik.stage_id = gonderildi_stage_no.id
                    print("Kontrol = 1")
                if kontrol == 0:
                    etkinlik.stage_id = gonderilemedi_stage_no.id
                    print("Etkinlik no2:", etkinlik.stage_id)
            self.env.cr.commit()
