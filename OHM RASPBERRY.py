#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import json
import requests
import urllib2
import time
import serial
import RPi.GPIO as gpio
import threading
import Adafruit_DHT
import socket
from neopixel import *





def pwmSet(args,stop):
	while (True):
		time.sleep(0.1) #tempo de time para envio gpio 40
		pwmFan.start(50) # inicio do dutycicle em 50%
		pwmFan.ChangeDutyCycle(args) #alteracao do dutycicle
		if stop():            	
				break	


def iniciarSerial():
	return serial.Serial(port='/dev/ttyS0', #porta comunicação raspberry tela nextion
  	baudrate = 9600,
  	parity=serial.PARITY_NONE,
  	stopbits=serial.STOPBITS_ONE,
  	bytesize=serial.EIGHTBITS,
  	timeout=1
	)


def replaceerro(args):
	dados=args
	i=0
	while i < 10:	
		dados = dados.encode('iso-8859-1').replace(','+str(i)+' %','')		#substitui caracteres dispensaveis no .json
		i+=1 #incremento do loop maximo 10
	return dados

def code(args):
	return args.encode('iso-8859-1')	#troca encode do texto

def preenchertela():		
		response = urllib2.urlopen(url) #captura .json
		jsond = json.loads(response.read())		#converte o texto .json web para objeto json python 
		for dados in jsond: #navega entre todos os objetos no json
			if 'Value' in json.dumps(jsond[dados['id']]): #verifica se o objeto possui o campo Value
				valor = dados['Value'] #atribui Value a variavel
				id = dados['id']       #atribui id a variavel
		                if id==28:
				        #WaterCooler rpm                            
					ser.write("waterrpm.txt=\""+code(valor)+"\""+EndCom)	
					udp.sendto("[rpm,"+code(valor)+"]",dest)
				elif id==39:
					#CPU Core #1"	                              
					ser.write("cpucore1.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[cpuCore01,"+code(valor)+"]",dest)		
				elif id==40:
					#CPU Core #2"	                              
					ser.write("cpucore2.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[cpuCore02,"+code(valor)+"]",dest)			
				elif id==41:
					#CPU Core #3"	                              
					ser.write("cpucore3.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[cpuCore03,"+code(valor)+"]",dest)								
				elif id==42:
					#CPU Core #4"	                              
					ser.write("cpucore4.txt=\""+code(valor)+"\""+EndCom)	
					udp.sendto("[cpuCore04,"+code(valor)+"]",dest)							
				elif id==43:
					#CPU Core #5"	                              
					ser.write("cpucore5.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[cpuCore05,"+code(valor)+"]",dest)									
				elif id==44:
					#CPU Core #6"	                              
					ser.write("cpucore6.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[cpuCore06,"+code(valor)+"]",dest)												
				elif id==52:
					#cpu package 36 C"	                              
					ser.write("cputemp.txt=\""+code(valor)+"\""+EndCom) 
					udp.sendto("[cpuTemp,"+code(valor)+"]",dest)														
				elif id==54:
					#cpu total usage"
					ser.write("cpuusage.val="+replaceerro(valor)+""+EndCom)
					udp.sendto("[cpuLoadTotal,"+replaceerro(valor)+"]",dest)																	
				elif id==74:
					#gpu core"	                              
					ser.write("gpucore.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[gpuCore,"+code(valor)+"]",dest)
				elif id==75:
					#gpumemory"	                              
					ser.write("gpumemory.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[gpuMemomy,"+code(valor)+"]",dest)
				elif id==76:
					#gpu shader"	                              
					ser.write("gpushader.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[gpuShader,"+code(valor)+"]",dest)
				elif id==78:
					#gpu core c"	                              
					ser.write("tempgpu.txt=\""+code(valor)+"\""+EndCom)
					udp.sendto("[gpuCoreTemp,"+code(valor)+"]",dest)
				elif id==80:
					#gpu core load"
					ser.write("gpucoreusage.val="+replaceerro(valor)+""+EndCom)
					udp.sendto("[gpuCoreLoad,"+replaceerro(valor)+"]",dest)
				elif id==81:
					#gpu core load"
					ser.write("gpucontrusage.val="+replaceerro(valor)+""+EndCom)
					udp.sendto("[gpuMemoryControlLoad,"+replaceerro(valor)+"]",dest)
				elif id==82:
					#gpu core load"
					ser.write("gpuvideousage.val="+replaceerro(valor)+""+EndCom)
					udp.sendto("[gpuVideoEngineLoad,"+replaceerro(valor)+"]",dest)
				elif id==83:
					#gpu core load"
					ser.write("gpumemusage.val="+replaceerro(valor)+""+EndCom)
					udp.sendto("[gpuMemoryLoad,"+replaceerro(valor)+"]",dest)






# animacao leds
def colorWipe(strip,color,stop):
	while (True):
		"""Wipe color across display a pixel at a time."""
		for i in range(strip.numPixels()):        
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(0.05)
		if stop():            	
			break	


#sensor umidade e temperatura
def sensorTempUmidade(pinoGpioDoSensor,tipoSensor):	
	HOST = '127.0.0.1'  # Endereco IP do Servidor
	PORT = 5000            # Porta que o Servidor esta
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (HOST,PORT)
	
	umidade,temperatura= Adafruit_DHT.read_retry(tipoSensor,pinoGpioDoSensor)
	temperatura = str(temperatura)
	umidade = str(umidade)
	ser.write("tempAmbiente.txt=\""+code(temperatura)+"\""+EndCom)
	udp.sendto("[tempAmbiente,"+code(temperatura)+"]",dest)
	ser.write("umidade.txt=\""+code(umidade)+"\""+EndCom)
	udp.sendto("[umidade,"+code(umidade)+"]",dest)
		


#tratamento erros do Hex
def tratamentoHex(args):
	if len(args) == 31:
		return int(args[4:-25],16) 		
	elif len(args) == 28: 
		return int(hex(ord(args[2:-25]))[2:],16) 

def serverTcpLocal(ser,stop):
	rpm = ""
	cpuCore01 = ""
	cpuCore02 = ""
	cpuCore03 = ""
	cpuCore04 = ""
	cpuCore05 = ""
	cpuCore06 = ""
	cpuTemp = ""
	cpuLoadTotal = ""
	gpuCore = ""
	gpuMemomy = ""
	gpuShader = ""
	gpuCoreTemp = ""
	gpuCoreLoad = ""
	gpuMemoryControlLoad = ""
	gpuVideoEngineLoad = ""
	gpuMemoryLoad = ""
	tempAmbiente = ""
	umidade = ""
	pwm= ""
	red= ""
	blue = ""
	green = ""
	brilho = ""



	HOST = ''              # Endereco IP do Servidor
	PORT = 5000            # Porta que o Servidor esta
	tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	orig = (HOST, PORT)
	tcp.bind(orig)
	tcp.listen(1)
	

	while True:
		if stop():
			con.close()        	
			break
    		con, cliente = tcp.accept()
    		print 'Concetado por', cliente		
    		while True:			
			if stop():
				con.close()        	
				break	
        		msg = con.recv(27)
			if not msg: 
				 break
        		if msg == "page0":
        			ser.write("page 0"+EndCom)
				break																				
        		elif msg == "page1":
        			ser.write("page 1"+EndCom)
        		elif msg == "page2":
        			ser.write("page 2"+EndCom)
			elif msg == "setFanpwm":
				valor=con.recv(1024)
				ser.write("page1.fanpwm.val="+replaceerro(valor)+""+EndCom)
				ser.write("page1.vPwm.val="+replaceerro(valor)+""+EndCom)
				ser.write("page0.vPwm.val="+replaceerro(valor)+""+EndCom)
				pwm=valor
			elif msg == "setRed":
				valor=con.recv(1024)
				ser.write("page2.nRed.val="+replaceerro(valor)+""+EndCom)
				ser.write("page2.red.val="+replaceerro(valor)+""+EndCom)
				ser.write("page0.vRed.val="+replaceerro(valor)+""+EndCom)
				red=valor
			elif msg == "setBlue":
				valor=con.recv(1024)
				ser.write("page2.nBlue.val="+replaceerro(valor)+""+EndCom)
				ser.write("page2.blue.val="+replaceerro(valor)+""+EndCom)
				ser.write("page0.vBlue.val="+replaceerro(valor)+""+EndCom)
				blue=valor
			elif msg == "setGreen":
				valor=con.recv(1024)
				ser.write("page2.nGreen.val="+replaceerro(valor)+""+EndCom)
				ser.write("page2.green.val="+replaceerro(valor)+""+EndCom)
				ser.write("page0.vGreen.val="+replaceerro(valor)+""+EndCom)
				green=valor
			elif msg == "setBrilho":
				valor=con.recv(1024)
				ser.write("page2.nBrilho.val="+replaceerro(valor)+""+EndCom)
				ser.write("page2.brilho.val="+replaceerro(valor)+""+EndCom)
				ser.write("page0.vBrilho.val="+replaceerro(valor)+""+EndCom)
				brilho=valor

			elif msg == "rpm":
				con.send(rpm)
			elif msg == "cpuCore01":
				con.send(cpuCore01)
			elif msg == "cpuCore02":
				con.send(cpuCore02)
			elif msg == "cpuCore03":
				con.send(cpuCore03)
			elif msg == "cpuCore04":
				con.send(cpuCore04)
			elif msg == "cpuCore05":
				con.send(cpuCore05)
			elif msg == "cpuCore06":
				con.send(cpuCore06)
			elif msg == "cpuTemp":
				con.send(cpuTemp)
			elif msg == "cpuLoadTotal":
				con.send(cpuLoadTotal)
			elif msg == "gpuCore":
				con.send(gpuCore)
			elif msg == "gpuMemomy":
				con.send(gpuMemomy)
			elif msg == "gpuShader":
				con.send(gpuShader)
			elif msg == "gpuCoreTemp":
				con.send(gpuCoreTemp)
			elif msg == "gpuCoreLoad":
				con.send(gpuCoreLoad)
			elif msg == "gpuMemoryControlLoad":
				con.send(gpuMemoryControlLoad)
			elif msg == "gpuVideoEngineLoad":
				con.send(gpuVideoEngineLoad)
			elif msg == "gpuMemoryLoad":
				con.send(gpuMemoryLoad)
			elif msg == "tempAmbiente":
				con.send(tempAmbiente)
			elif msg == "umidade":
				con.send(umidade)
			elif msg == "pwm":
				con.send(pwm)
			elif msg == "red":
				con.send(red)
			elif msg == "blue":
				con.send(blue)
			elif msg == "green":
				con.send(green)
			elif msg == "brilho":
				con.send(brilho)

			elif msg == "getDados":	
					udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)	
					udp.bind(orig)		
					for x in range(0, 25):
						atualValor = (udp.recvfrom(27)[0])	
						print atualValor						
						if "rpm" in atualValor:
							rpm = splitDados(atualValor)
						elif "cpuCore01" in atualValor:
						 	cpuCore01 = splitDados(atualValor)
						elif "cpuCore02" in atualValor:
						 	cpuCore02 = splitDados(atualValor)
						elif "cpuCore03" in atualValor:
						 	cpuCore03 = splitDados(atualValor)
						elif "cpuCore04" in atualValor:
						 	cpuCore04 = splitDados(atualValor)
						elif "cpuCore05" in atualValor:
						 	cpuCore05 = splitDados(atualValor)
						elif "cpuCore06" in atualValor:
						 	cpuCore06 = splitDados(atualValor)
						elif "cpuTemp" in atualValor:
						 	cpuTemp = splitDados(atualValor)
						elif "cpuLoadTotal" in atualValor:
						 	cpuLoadTotal = splitDados(atualValor)
						elif "gpuCore" in atualValor:
						 	gpuCore = splitDados(atualValor)
						elif "gpuMemomy" in atualValor:
						 	gpuMemomy = splitDados(atualValor)
						elif "gpuCoreTemp" in atualValor:
						 	gpuCoreTemp = splitDados(atualValor)
						elif "gpuCoreLoad" in atualValor:
						 	gpuCoreLoad = splitDados(atualValor)
						elif "gpuMemoryControlLoad" in atualValor:
						 	gpuMemoryControlLoad = splitDados(atualValor)
						elif "gpuVideoEngineLoad" in atualValor:
						 	gpuVideoEngineLoad = splitDados(atualValor)
						elif "gpuMemoryLoad" in atualValor:
						 	gpuMemoryLoad = splitDados(atualValor)
						elif "tempAmbiente" in atualValor:
						 	tempAmbiente = splitDados(atualValor)
						elif "umidade" in atualValor:
							udp.close()
						 	umidade = splitDados(atualValor)
							break
						elif "pwm" in atualValor:
							udp.close()		
						 	pwm = splitDados(atualValor)	
							break
						elif "red" in atualValor:
						 	red = splitDados(atualValor)
						elif "blue" in atualValor:
						 	blue = splitDados(atualValor)
						elif "green" in atualValor:							
						 	green = splitDados(atualValor)
						elif "brilho" in atualValor:
							udp.close()
						 	brilho = splitDados(atualValor)
							break
						
						else:
							atualValor=""											
			else:
			  	msg = ""

			
				
			

#split do udp
def splitDados(args):
	return (args.split(",")[1])[:-1]
		
				
				
			


    							

if __name__ == '__main__':	
	gpio.setwarnings(False) #desativa mensagem de perigo gpio
	gpio.setmode(gpio.BOARD)
	ser = iniciarSerial()	#chama funcao para iniciar serial

   	 #dados pc
	url = ("http://192.168.2.235:8085/data.json") #url dados pc
	EndCom = "\xff\xff\xff" #final de write do nextion

	
	#pwm
	stop_threads_pwm = False #False para parar Theread
	gpio.setup(40,gpio.OUT) #gpio 40 saida pwm coole
	pwmFan = gpio.PWM(40,50) #define valor inicial
	pwmValue = 50 #valor padrao pwm
	pwm = threading.Thread(target=pwmSet,args=(pwmValue,lambda: stop_threads_pwm) )	 #cria Thread
	pwm.setDaemon(True)
	pwm.start()	 #inicia Theread
	
	
	# LED
	LED_COUNT      = 28   # numero de leds
	LED_PIN        = 18      # gpio 18 para pwm
	#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
	LED_FREQ_HZ    = 800000  # frequencia das leds default 800hz
	LED_DMA        = 10      # canal dma para gerar sinal deixar 10
	LED_BRIGHTNESS = 255    #  brilho 0 baixo 255 alto
	LED_INVERT     = False   # True para inverter polaridade
	LED_CHANNEL    = 0       # trocar por '1' para usar GPIOs 13, 19, 41, 45 ou 53    	
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL) # cria objeto NeoPixel    	
   	strip.begin() # inicializa biblioteca	
	stop_threads_leds = False #False para parar Theread
	ledRed = 255
	ledBlue = 255
	ledGreen = 0
	leds = threading.Thread(target=colorWipe,args=(strip, Color(ledGreen,ledRed,ledBlue),lambda: stop_threads_leds) ) #cria nova thread	
	leds.setDaemon(True)
	leds.start()	 #inicia Theread



	stop_threads_tcp = False #False para parar Theread
	serverTcp = threading.Thread(target=serverTcpLocal,args=(ser,lambda: stop_threads_tcp)) #cria nova thread	
	serverTcp.setDaemon(True)	
	serverTcp.start()	 #inicia Theread


	HOST = '127.0.0.1'  # Endereco IP do Servidor
	PORT = 5000            # Porta que o Servidor esta
	udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	dest = (HOST, PORT)

	try:		
		while(True):
		
			ser.write('sendme'+EndCom) #verifica qual tela nextion esta
			numeroTela = code(repr(ser.readline())) #pega o numero da tela
			if 'x00' in numeroTela:		# se for na tela 00 preencher dados pc
				preenchertela()					
				tempUmidade=threading.Thread(target=sensorTempUmidade,args=(25,Adafruit_DHT.DHT11) ) #inicia Theread umidade e temperatura local
				tempUmidade.setDaemon(True)
				tempUmidade.start()	 #inicia Theread
	
				
			elif 'x01' in numeroTela:
				ser.write('get page1.vPwm.val'+EndCom) #se for na tela 01 pedir valor da variavel que contem o pwm
				pwmAtual= tratamentoHex(repr(ser.readline()))  #pega valor somente do pwm			
				if pwmAtual in range(0,256):
					if pwmValue != pwmAtual: #se o pwm for diferente do atual seta novo pwm a thread
						pwmValue = pwmAtual	  #atribiu novo pwm						
						stop_threads_pwm = True #atribui para thread
						pwm.join()  #para thread
						stop_threads_pwm = False #cancela parada thread
						pwm = threading.Thread(target=pwmSet,args=(pwmValue,lambda: stop_threads_pwm) ) #cria nova thread
						pwm.setDaemon(True)
						pwm.start()			   #inicia nova thread
				udp.sendto("[pwm,"+str(pwmValue)+"]",dest)


			elif 'x02' in numeroTela:
							
				ser.write('get page2.nRed.val'+EndCom) #valor led vermelha
				tempRed=tratamentoHex(repr(ser.readline())) #tratamento de excessao
				

				ser.write('get page2.nBlue.val'+EndCom) #valor led azul
				tempBlue=tratamentoHex(repr(ser.readline())) #tratamento de excessao		
				

				ser.write('get page2.nGreen.val'+EndCom) #valor led verde
				tempGreen=tratamentoHex(repr(ser.readline())) #tratamento de excessao
				

				ser.write('get page2.nBrilho.val'+EndCom) #valor led verde
				tempBrilho=tratamentoHex(repr(ser.readline())) #tratamento de excessao
				

	
				if ledRed != tempRed or ledBlue != tempBlue or ledGreen != tempGreen or LED_BRIGHTNESS != tempBrilho: #tratamento de excessao	
				
					if tempRed in range(0,256) and tempBlue in range(0,256) and tempGreen in range(0,256) and tempBrilho in range(0,256):
						ledRed=tempRed
						ledBlue=tempBlue
						ledGreen=tempGreen
					    LED_BRIGHTNESS = tempBrilho
						stop_threads_leds = True #True para parar Theread
						leds.join()
						stop_threads_leds = False #False para parar Theread
						strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL) # cria objeto NeoPixel    	
   						strip.begin() # inicializa biblioteca
						leds = threading.Thread(target=colorWipe,args=(strip, Color(ledGreen,ledRed,ledBlue),lambda: stop_threads_leds) ) #cria nova thread
						leds.setDaemon(True)
						leds.start()
			
				udp.sendto("[red,"+str(ledRed)+"]",dest)
				udp.sendto("[blue,"+str(ledBlue)+"]",dest)
				udp.sendto("[green,"+str(ledGreen)+"]",dest)
				udp.sendto("[brilho,"+str(LED_BRIGHTNESS)+"]",dest)
	
				
		
			

	except ValueError:
		pass
	except KeyboardInterrupt:
		pass						
		stop_threads_pwm = True #atribui para thread
	    pwm.join()          #para thread
		stop_threads_leds = True
		leds.join()
		stop_threads_leds = False
		leds = threading.Thread(target=colorWipe,args=(strip, Color(0,0,0),lambda: stop_threads_leds) ) #cria nova thread
		leds.setDaemon(True)
		leds.start()
		time.sleep(5)
		stop_threads_leds = True
		leds.join()		
		stop_threads_tcp = True #False para parar Theread
		serverTcp.join()

		