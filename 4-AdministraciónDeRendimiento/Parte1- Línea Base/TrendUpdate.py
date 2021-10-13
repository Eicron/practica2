import time
import rrdtool
from getSNMP import consultaSNMP
from threading import Thread
from trendGraphDetection import grafica
from inventarioPDF import creaPDF
from  Notify import send_alert_attached
import time

rrdpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/RRD/'
carga_CPU = 0

i = 0


def sentinela (n):
    global i
    while 1:
        if i >=80:
            print('mas de 70')
            time.sleep(30)
            grafica()
            #time.sleep(10)
            #send_alert_attached("El uso de procesador ha sobrepasado la recomendación")
            #print("El uso de procesador ha sobrepasado la recomendación")
            #infoDisp = consultaSNMP2('comunidadASR','localhost','1.3.6.1.2.1.1.1.0')
            #creaPDF(infoDisp, 'deteccion.png')            
            time.sleep(120)

t = Thread(target = sentinela, args=(10, ), daemon=True )
t.start()


while 1:
    
    carga_CPU = int(consultaSNMP('comunidadASR','192.168.0.8','1.3.6.1.2.1.25.3.3.1.2.196608'))
    valor = "N:" + str(carga_CPU)
    i = carga_CPU
    print (valor)
    rrdtool.update(rrdpath+'trend.rrd', valor)
    rrdtool.dump(rrdpath+'trend.rrd','trend.xml')
    time.sleep(5)

if ret:
    print (rrdtool.error())
    time.sleep(300)
