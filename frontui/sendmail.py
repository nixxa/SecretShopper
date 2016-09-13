""" Send email """
import os
import logging
import re
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content


class MailProvider:
    """ Provider for sending e-mails """
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        self.email_pattern = ''
        return
    
    def send_checklist_notice(self, author_mail, checklist):
        # check email 
        match = re.match(r'^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', author_mail)
        if match == None:
            logging.error('E-mail adddress %s is wrong', author_mail)
            return
        sg = sendgrid.SendGridAPIClient(apikey=self.api_key)
        from_email = Email('noreply@secret-shopper.azurewebsites.net')
        to_email = Email(author_mail)
        subject = "[SecretShopper] АЗС #{0}".format(checklist.object_info.num)
        body = "<h2>Контрольный лист посещения сохранен</h2>\
            <p>Для исправления анкеты необходимо перейти по ссылке \
            <a href='http://secret-shopper.azurewebsites.net/checklist/edit/{0}'>http://secret-shopper.azurewebsites.net/checklist/edit/{0}</a></p>\
            <p>Для добавления файлов воспользуйтесь ссылкой \
            <a href='http://secret-shopper.azurewebsites.net/checklist/addfiles/{0}'>http://secret-shopper.azurewebsites.net/checklist/addfiles/{0}</a></p>\
            <p><br/><br/><br/><br/><br/><hr /><small>Это сообщение сформировано автоматически, на него не нужно отвечать.</small></p>".format(checklist.uid)
        content = Content("text/html", body)
        mail = Mail(from_email, subject, to_email, content)
        mail_response = sg.client.mail.send.post(request_body=mail.get())
        if mail_response.status_code != 202:
            logging.error('Cant send email. Error is "%s"', mail_response.body)
        return