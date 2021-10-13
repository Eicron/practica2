import sys
import rrdtool
from  Notify import send_alert_attached
from inventarioPDF import creaPDF
from getSNMP import consultaSNMP2


def grafica ():
    rrdpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/RRD/'
    imgpath = '/home/eric/ASR/Practicas/Practica2/4-AdministraciónDeRendimiento/IMG/'

    ultima_lectura = int(rrdtool.last(rrdpath+"trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 600
    imgName = 'deteccion.png'


    ret = rrdtool.graphv( imgpath+imgName,
                        "--start",str(tiempo_inicial),
                        "--end",str(tiempo_final),
                        "--vertical-label=Cpu load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "--title=Uso del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",

                        "DEF:cargaCPU="+rrdpath+"trend.rrd:CPUload:AVERAGE",

                        "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                        "VDEF:cargaMIN=cargaCPU,MINIMUM",
                        "VDEF:cargaSTDEV=cargaCPU,STDEV",
                        "VDEF:cargaLAST=cargaCPU,LAST",

                        "LINE10:60#ff000020",
                        "LINE10:70#ff000040",
                        "CDEF:umbral5=cargaCPU,70,LT,0,cargaCPU,IF",
                        "AREA:cargaCPU#00FF00:Carga del CPU",
                        "AREA:umbral5#FF9F00:Carga CPU mayor que 70",
                        "HRULE:70#FF0000:Umbral 1 - 5%",

                        "PRINT:cargaLAST:%6.2lf",
                        "GPRINT:cargaMIN:%6.2lf %SMIN",
                        "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                        "GPRINT:cargaLAST:%6.2lf %SLAST" )
    
    print (ret)

    ultimo_valor=float(ret['print[0]'])
    if ultimo_valor>70:
        infoDisp = consultaSNMP2('comunidadASR','192.168.0.8','1.3.6.1.2.1.1.1.0')
        creaPDF(infoDisp, imgName)  
        send_alert_attached("El uso de procesador ha sobrepasado la recomendación")
        print("El uso de procesador ha sobrepasado la recomendación")
    
        
    