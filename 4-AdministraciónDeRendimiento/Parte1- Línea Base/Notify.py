import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getSNMP import consultaSNMP2
from inventarioPDF import acomodaInfo

COMMASPACE = ', '
# Define params  /home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento
rrdpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/RRD/'
imgpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/IMG/'
fname = 'trend.rrd'

infoDisp = consultaSNMP2('comunidadASR','192.168.0.8','1.3.6.1.2.1.1.1.0')
info = acomodaInfo(infoDisp)


mailsender = "sesionesio2020@gmail.com"
mailreceip = "tanibet.escom@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = '3spartanInteligencia.'

def send_alert_attached(subject):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    mensaje = 'El uso del procesador ha sobre pasado el umbral para el dispositivo\n'+ info
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open(imgpath+'deteccion.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    msg.attach(MIMEText(mensaje,'plain'))
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()