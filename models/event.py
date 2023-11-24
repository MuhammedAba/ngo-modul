from odoo import models, fields, api
from odoo.exceptions import ValidationError

class EventEvent(models.Model):
    _inherit = "event.event"
    _description = "Event"

    project_skills = fields.Many2many(
        "project.skills", string="Proje Yetenekleri"
    )
    tetiklendi_flag = fields.Boolean(default=True)

    @api.onchange('stage_id')
    def on_change_stage(self):
        kontrol = 0
        gonderiliyor_stage_no = self.env['event.stage'].search(args=[('name', '=', 'Mail Gönderiliyor')])
        etkinlikler = self.env['event.event'].search(args=[('stage_id', '=', gonderiliyor_stage_no.id)])

        gonderildi_stage_no = self.env['event.stage'].search(args=[('name', '=', 'Mail Gönderildi')])
        gonderilemedi_stage_no = self.env['event.stage'].search(args=[('name', '=', 'Mail Gönderilemedi')])
        
        print("***********************************: ",len(etkinlikler))
        if(len(etkinlikler) > 0):   
            for etkinlik in etkinlikler:
                print("Etkinlik no1:",etkinlik.stage_id)
                if(kontrol ==1):
                    etkinlik.stage_id = gonderildi_stage_no.id
                    print("Kontrol = 1")
                if(kontrol == 0):
                    etkinlik.stage_id = gonderilemedi_stage_no.id
                    print("Etkinlik no2:",etkinlik.stage_id)
            self.env.cr.commit()




            # Event'in tag alanındaki değerleri al
            #event_tags = self.tag_ids.mapped('name')

    #         # Contact modelindeki yetenekler alanındaki değeri al (varsayılan olarak 'partner_id' ile ilişkilendirilmiş kişiyi kullanıyoruz)
    #         contact_tags = self.partner_id.yetenekler

    #         # Eğer bir eşleşme varsa, kullanıcıya e-posta gonder
    #         if set(event_tags) & set(contact_tags):
    #             self.send_email_to_user()

    # def send_email_to_user(self):
    #     body = "Dear,Type your content" 
    # mail_values = {
    #     'email_to': partner.email,
    #     'subject': subject,
    #     'body_html': body,
    #     'state': 'outgoing',
    #     'type': 'email',
    #     }
    
    # mail_id = mail.mail.create(mail_values)
    # mail_id.send()

