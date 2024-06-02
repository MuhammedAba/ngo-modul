from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EventEvent(models.Model):
    _inherit = "event.event"
    _description = "Event"

    project_skills = fields.Many2many("project.skills", string="Proje Yetenekleri")
    test1=fields.Char("Test for event")
   

    @api.onchange("stage_id")
    def on_change_stage(self):
        partners = self.env["res.partner"].search([])
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
                if partner.volunteer_skills.id == event.tag_ids.id: #id'ye göre eşleme yapılıyor. 
                    print(
                        "*************************************************\n"
                        + f"Eşleşen Kayıt - Partner: {partner.name}, Event: {event.name}"
                        + "\n*************************************************\n"
                    )
                    # E-posta gönderme metodu çağrılıyor
                    self.send_email_to_user(partner, event)

        if len(etkinlikler) > 0:
            for etkinlik in etkinlikler:
                print("+++++++++++++++++++",etkinlik.test1)
                if etkinlik.test1=="Doğru":
                    etkinlik.stage_id = gonderildi_stage_no.id
                else:
                    etkinlik.stage_id = gonderilemedi_stage_no.id
            self.env.cr.commit()

    def send_email_to_user(self, partner, event):
        print(f"Mail Gönderilen Kisinin Maili : {partner.email}\n ")
        body = (
            """
            Merhabalar kuruluşumuzda eklediğiniz yetenek ile bu hafta eklenen etkinliğimizde ihtiyac duyulan  yetenek eşleşmiştir.
            En kısa sürede aşağıda belirtilen linke tıklayarak etkinliğe ulaşıp kayıt  yapabilirsiniz.
            İyi günler...\n"""
            + "\nEtkinlik ismi : "
            + event.name
            + "\nEtkinliğe ulaşmak için linke tıklayın: <a href='http://localhost:8069"
            + event.website_url
            + "'>Etkinlik Linki</a>"
        )
        mail_values = {
            "email_to": partner.email,
            "body_html": body,
            "subject": "Etkinlik Bilgilendirmesi",
            "state": "outgoing",
        }

        mail = self.env["mail.mail"].create(mail_values)
        mail.send()

        if mail.state == "sent":
            event.write({"test1": "Doğru"})
            print("++++++++++++++++++++++++++\nMailler gönderildi.\n++++++++++++++++++++++++++++ ")
