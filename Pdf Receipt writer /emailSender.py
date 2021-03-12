import smtplib 
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os.path
class EmailSender(): 
    def send_email(self, email_recipients, email_subject,email_credentials_path, bcc_recipients=[], attachment_location=''): 
        '''
        Function to send an email.
        Inputs: 
         -email_recipients: The list of email recipients 
         -email_subject: The email subject 
         -bcc_recipients: The list of bcc recipients 
         -email_credentials_path: Path to the file that contains the email credentials
         -attachment_location: The location of the attached file
        '''
        email_message = '''Buen día,

adjunto envío la cuenta de cobro por concepto "Distribución resultados participación U.T. PROSUEÑO  COLOMBIA según contrato por suministro equipos programa de atención integral pacientes con apnea de sueño  EPS-Sanitas"


Quedo atento a cualquier inquietud e instrucción.

Cordialmente,

Cristhian Sánchez'''
        email_sender,password = self.get_email_credentials(email_credentials_path)
        msg = MIMEMultipart()
        msg['From'] = 'Cristhian Camilo Sánchez Fino' 
        msg['To'] = ', '.join(email_recipients)
        msg['Subject'] = email_subject 
        msg['Bcc'] = ', '.join(bcc_recipients)
        msg.attach(MIMEText(email_message,'plain'))        
        if attachment_location !='': 
            filename = os.path.basename(attachment_location)
            attachment = open(attachment_location,'rb')
            part = MIMEApplication(attachment.read())
            part.add_header('Content-Disposition','attachment', filename= filename)
            msg.attach(part)
            try: 
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.ehlo()
                server.starttls()
                server.login(email_sender,password)
                text = msg.as_string()
                server.sendmail(email_sender,(email_recipients+bcc_recipients),text)
                server.quit()
            except : 
                print('SMPT server connection error')
            return True
    def get_email_credentials(self,filepath=''): 
        '''Function that retrieves the email credentials from the file path
        Inputs: 
        - filepath: path to the file with the email credentials 
        '''
        with open(filepath,"r") as reader: 
            text_content = reader.read()
        email,password = text_content.split(':')
        return email, password 

