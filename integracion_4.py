import smbus
import time
import os
import base64
import uuid
import json
import sys
import board
import busio
import eel
import requests
import subprocess
import random
import RPi.GPIO as GPIO
from datetime import datetime as dt
from datetime import datetime

# Funcion para consegir la direccion Mac Address del dispositivo 
from uuid import getnode as get_mac
mac = get_mac()
print(mac)
print(hex(mac))
macString = ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))
print('[' + macString + ']')

# inicialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

# inicio del servicio de la AppWeb
eel.init('web2.1')
eel.start("index.html", block=False , cmdline_args=['--kiosk'])  # Start
#eel.start("index.html", mode="chrome", block=False )  # Start
   
# variables estaticas
listaTemporal = []
i = 0
RS = 0
RL = 1.0
Clean_Air_Ratio = 28.943
connectedIOT = 0
numListTem = 0
mqttConnet = 0  

while True:
# valores random para llenado de datos de los sensores
	cTemp = random.randrange(5, 27, 4)
	humidity = random.randrange(5, 27, 4)
	COppm = random.randrange(5, 27, 4)
	Microph_dbZ = random.randrange(5, 27, 4)
	Microph_dbA = random.randrange(5, 27, 4) 
	Microph_dbC = random.randrange(5, 27, 4)
	latitud = random.randrange(5, 27, 4)
	longitud = random.randrange(5, 27, 4)
	acelX = random.randrange(5, 27, 4)
	acelY = random.randrange(5, 27, 4)
	acelZ = random.randrange(5, 27, 4)
	valoresPms1 = random.randrange(5, 27, 4)
	valoresPms2_5 = random.randrange(5, 27, 4) 
	valoresPms10 = random.randrange(5, 27, 4)
	
	# Fecha y hora de la toma de
	now = datetime.now()
	
	# verificacion de datos en consola
	print("--------Meter--------------------")
	print('Mac address = [' + macString + ']')
	print("Temperature: ", cTemp, "°C")
	print("Humidity   : ", humidity,"%HR")
	print("CO : ", COppm, "ppm")
#	print("PM 1.0 =", dic['pm1_0cf1'], " PM 2.5 =", dic['pm2_5cf1'], " PM 10 =", dic['pm10cf1'])
	print("Microphone : ", Microph_dbZ, "dBZ")
	print("Microphone : ", Microph_dbA, "dBA")
	print("Microphone : ", Microph_dbC, "dBC")
	print("latitud_GPS : ", latitud, "lat")
	print("longitud_GPS : ", longitud, "lon")
#	print("cordenada :", valorSIM)
	print("eje X =", acelX, " eje Y =", acelY, " eje Z", acelZ)
	print("fecha/hora = ", now)
	print("---------------------------------")
	
	i = i + 1
	print('Publicacion al Topic "conhintec/medidor" numero: ', i)
	
	# construir Json manejo de datos
# 	message = {}
# 	message['Mac'] = str('[' + macString + ']')
# 	message['temp'] = str(cTemp)
# 	message['humi'] = str(humidity)
# 	message['co'] = str(COppm)
# 	message['dBZ'] = str(Microph_dbZ)
# 	message['dBA'] = str(Microph_dbA)
# 	message['dBC'] = str(Microph_dbC)
# 	message['pm_1.0'] = str(dic['pm1_0cf1'])
# 	message['pm_2.5'] = str(dic['pm2_5cf1'])
# 	message['pm_10'] = str(dic['pm10cf1'])
# 	message['lat'] = str(latitud)
# 	message['lon'] = str(longitud)
# 	message['eje_X'] = str(acelX)
# 	message['eje_Y'] = str(acelY)
# 	message['eje_Z'] = str(acelZ)
# 	message['fecha/hora'] = str(now)
# 	messageJson = json.dumps(message)
	
	
	# Envio de datos por medio de EEL al servicio AppWeb     
	timestamp = dt.now()
	eel.addTextMac("Mac  = {}".format(str(macString)))
	eel.addTextTemp("temperatura = {} °C".format(str(cTemp)))
	eel.addTextHum("humedad = {} %Hr".format(str(humidity)))
	eel.addTextCo("CO  = {} ppm".format(str(COppm)))
	eel.addTextPms("Pms 1.0 = {} ppm".format(str(valoresPms1)))
	eel.addTextPms2("Pms 2.5 = {} ppm".format(str(valoresPms2_5)))
	eel.addTextPms10("Pms 10 = {} ppm".format(str(valoresPms10)))
	eel.addTextdbZ(format(str(Microph_dbZ)))
	eel.addTextdbA("Microfono = {} dBA".format(str(Microph_dbA)))
	eel.addTextdbC("Microfono = {} dBC".format(str(Microph_dbC)))
	eel.addTextEjeX("eje X  = {} x".format(str(acelX)))
	eel.addTextEjeY("eje Y  = {} y".format(str(acelY)))
	eel.addTextEjeZ("eje Z  = {} z".format(str(acelZ)))
	eel.addTextTime("fecha/hora  = {} ".format(str(now)))
	eel.sleep(0.5)
	
# 	if i == 2:
# 		# inicio del servicio de la AppWeb
# 		#eel.init('web2')
# 		eel.start("index.html", block=False , cmdline_args=['--kiosk'])  # Start
# 		#eel.start("index.html", block=False )  # Start
	
#	time.sleep(0.2)
	
	


