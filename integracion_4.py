import csv
import smbus
import time
import os
import base64
import uuid
import json
import sys
import datetime
import board
import busio
import eel
import mh_z19
import requests
import subprocess
import RPi.GPIO as GPIO
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from datetime import datetime as dt
from pms7003 import Pms7003Sensor, PmsSensorException
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient  # libreria amazon AWS IoT
from microf_barras1 import MicrofonoPlacid
#from leddCode import colores
from accelerometer import acel
from datetime import datetime
#from SIM868 import SIM

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

# AWS IoT 
# suscripcion y validacion de certificaciones 
myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint("a1gpptc672aj5e-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi02/Gauges/Cer_aws-iot/AmazonRoot_CA1.pem",
                                  "/home/pi02/Gauges/Cer_aws-iot/e8b6e32aef1db82d8a37c5fcf01b4dcc06599fd1fc1c89a8f97794a2af071617-private.pem.key",
                                  "/home/pi02/Gauges/Cer_aws-iot/e8b6e32aef1db82d8a37c5fcf01b4dcc06599fd1fc1c89a8f97794a2af071617-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)

# inicio del servicio de la AppWeb
# eel.init('web2')
# eel.start("index.html", block=False, cmdline_args=['--kiosk'])  # Start
# time.sleep(2)
# eel.start("index.html", block=False, disable_cache=True, cmdline_args=['--kiosk'])  # Start
#eel.start("index.html", mode="chrome", block=False )  # Start

# Configuracion sensores analogos a digitales
i2c = busio.I2C(board.SCL, board.SDA)               # creando el ADC objeto usando I2C bus
ads = ADS.ADS1015(i2c)
ads.gain = 1

# creando variables para la lectura del mudulo ADS 
chan = AnalogIn(ads, ADS.P0)

# coneccion puerto seriar conecccion PMS7003 y obtension de datos
sensor = Pms7003Sensor('/dev/ttyUSB0')
dic = sensor.read()
    
# variables estaticas
listaTemporal = []
i = 0
RS = 0
RL = 1.0
Clean_Air_Ratio = 28.943
connectedIOT = 0
numListTem = 0
mqttConnet = 0
#mensaje = None

# def customCallback(client, userdata, message):
#     global mensaje
#     mensaje = str(message.payload)

while True:
	
	# Lectura I2C sensor Temp y Humd, calibracion de ambos
	bus = smbus.SMBus(1)
	bus.write_i2c_block_data(0x44, 0x2C, [0x0D]) 
#	time.sleep(0.5)
	data = bus.read_i2c_block_data(0x44, 0x00, 6)
	temp = data[0] * 256 + data[1]                     # Convert the data
	cTemp = round(-45 + (175 * temp / 65535.0), 2)     # formulas deifinidas por el fabricante del sensor
	humidity = round((100 * (data[3] * 256 + data[4]) / 65535.0),2)
	
	if 70 < i < 150:
		cTemp = cTemp - 3
	elif 150 < i < 250:
		cTemp = cTemp - 7
	elif 250 < i < 350:
		cTemp = cTemp - 10
	elif 350 < i < 450:
		cTemp = cTemp - 14
	cTemp = round(cTemp, 2)
	
	RS = 1000 * ((5 - chan.voltage)/chan.voltage)
	COppm1 = 29.919 * pow(RS/31040, -0.668)
	COppm = round(COppm1, 2)
	
	mh_z19.read_all()
	
	# datos Pms guardado en constantes
	valoresPms1 =  dic['pm1_0cf1']
	valoresPms2_5 =  dic['pm2_5cf1']
	valoresPms10 =  dic['pm10cf1']
	
	# llama la funcion Prueba() y se almacena dato Hz en ValorMicroph
#	try:
#	ValorMicroph = MicrofonoPlacid()
	MicrofonoPlacid()
# 	except:
# 		print("microfono desbordado..........")        
# 	Microph_dbA = ValorMicroph[1]
# 	Microph_dbA = round(Microph_dbA, 2)
# 	Microph_dbZ = ValorMicroph[0]
# 	Microph_dbZ = round(Microph_dbZ, 2)
# 	Microph_dbC = ValorMicroph[2]
# 	Microph_dbC = round(Microph_dbZ, 2)
	
	# llama la funcion SIM868(), se almacena valor latitud y longitud
	#valorSIM = SIM()
	latitud = 0.0
	latutud = round(latitud, 2)
	longitud = 0.0
	longitud = round(longitud, 2)
	
	# llama la funcion acel(), se almacena los ejes(X, Y, Z)
	try:
		valorAcel = acel()
	except:
		print("microfono desbordado..........")  
	acelX = valorAcel[0]
	acelX = round(acelX, 2)
	acelY = valorAcel[1]
	acelY = round(acelY, 2)
	acelZ = valorAcel[2]
	acelZ = round(acelZ, 2)
	
	# Fecha y hora de la toma de datos
	now = datetime.now()
	
# 	place = ['cosina']
# 	
# 	with open('saveGlobal.csv', 'w', encoding='UTF8', newline='') as file:
# 		writer = csv.writer(file)
# 		writer.writerow(place)
# 		
# 	with open('saveGlobal.csv', 'r') as file:
# 		reader = csv.reader(file)
# 		for row in reader:
# 			plac = row            
	
# 	# verificacion de datos en consola
# 	print("--------Meter--------------------")
# 	print('Mac address = [' + macString + ']')
# 	print("Temperature: ", cTemp, "°C")
# 	print("Humidity   : ", humidity,"%HR")
# #	print("CO :{:>5}\t{:>5.5f}".format(chan.value, chan.voltage))
# 	print("CO : ", COppm, "ppm")
# 	print("PM 1.0 =", dic['pm1_0cf1'], " PM 2.5 =", dic['pm2_5cf1'], " PM 10 =", dic['pm10cf1'])
# 	print("Microphone : ", Microph_dbZ, "dBZ")
# 	print("Microphone : ", Microph_dbA, "dBA")
# 	print("Microphone : ", Microph_dbC, "dBC")
# 	print("latitud_GPS : ", latitud, "lat")
# 	print("longitud_GPS : ", longitud, "lon")
# #	print("cordenada :", valorSIM)
# 	print("eje X =", acelX, " eje Y =", acelY, " eje Z", acelZ)
# #	print("lugar = ", plac)
# 	print("fecha/hora = ", now)
# 	print("---------------------------------")
	
	i = i + 1
	print('Publicacion al Topic "conhintec/medidor" numero: ', i)
	
	#colores()
			# Envio de datos por medio de EEL al servicio AppWeb
	      
# 	timestamp = dt.now()
# 	eel.addTextMac("Mac  = {}".format(str(macString)))
# 	eel.addTextTemp("temperatura = {} °C".format(str(cTemp)))
# 	eel.addTextHum("humedad = {} %Hr".format(str(humidity)))
# 	eel.addTextCo("CO  = {} ppm".format(str(COppm)))
# 	eel.addTextPms("Pms 1.0 = {} ppm".format(str(valoresPms1)))
# 	eel.addTextPms2("Pms 2.5 = {} ppm".format(str(valoresPms2_5)))
# 	eel.addTextPms10("Pms 10 = {} ppm".format(str(valoresPms10)))
# #	eel.addTextdbZ("Microfono = {} dBZ".format(str(Microph_dbZ)))
# 	eel.addTextdbZ((str(Microph_dbZ)))
# 	eel.addTextdbA("Microfono = {} dBA".format(str(Microph_dbA)))
# 	eel.addTextdbC("Microfono = {} dBC".format(str(Microph_dbC)))
# 	eel.addTextEjeX("eje X  = {} x".format(str(acelX)))
# 	eel.addTextEjeY("eje Y  = {} y".format(str(acelY)))
# 	eel.addTextEjeZ("eje Z  = {} z".format(str(acelZ)))
# 	eel.addTextTime("fecha/hora  = {} ".format(str(now)))
# 	eel.sleep(0.4)
	
# 	# construir Json manejo de datos
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
# 	
# 	try:
# 		if myMQTTClient.connect():
# 			if mqttConnet == 0:            
# 				print(myMQTTClient.connect())        
# 				myMQTTClient.connect()
# 				time.sleep(1.5)
# 				mqttConnet = 1  
# 		
# 		# Almacenar datos Json en una list, si el dispositivo no tiene coneccion ala Red
# 		if numListTem == 1:
# 			messageJsonList = json.dumps(listaTemporal)
# 			myMQTTClient.publish("esp32/pub", messageJsonList, 0)        # AWS Brouker IoT        
# 			print("+++++ se manda lista mqtt ++++++")
# 			listaTemporal.clear()
# 			numListTem = 0
# 		
# 	# Protocolo MQTT de envio Json al Topic
# 		myMQTTClient.publish("esp32/pub", messageJson, 0)        # AWS Brouker IoT
# 	
# 	except:
# 		listaTemporal.append(messageJson)
# 		numListTem = 1
# 		print("CACHE LIST = ", listaTemporal, len(listaTemporal))
# 		mqttConnet = 0  
	
#	if i == 70:
		# inicio del servicio de la AppWeb
		#eel.init('web2')
		#eel.start("index.html", block=False, cmdline_args=['--kiosk'])  # Start
#		eel.start("index.html")  # Start
	
#	time.sleep(0.2)
	
	


