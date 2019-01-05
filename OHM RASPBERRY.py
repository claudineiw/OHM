#!/usr/bin/env python2
# coding: utf-8
import json
import requests
import urllib2
import time
import serial
import RPi.GPIO as gpio
import threading
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
				elif id==39:
					#CPU Core #1"	                              
					ser.write("cpucore1.txt=\""+code(valor)+"\""+EndCom)				
				elif id==40:
					#CPU Core #2"	                              
					ser.write("cpucore2.txt=\""+code(valor)+"\""+EndCom)					
				elif id==41:
					#CPU Core #3"	                              
					ser.write("cpucore3.txt=\""+code(valor)+"\""+EndCom)							
				elif id==42:
					#CPU Core #4"	                              
					ser.write("cpucore4.txt=\""+code(valor)+"\""+EndCom)									
				elif id==43:
					#CPU Core #5"	                              
					ser.write("cpucore5.txt=\""+code(valor)+"\""+EndCom)										
				elif id==44:
					#CPU Core #6"	                              
					ser.write("cpucore6.txt=\""+code(valor)+"\""+EndCom)														
				elif id==52:
					#cpu package 36 C"	                              
					ser.write("cputemp.txt=\""+code(valor)+"\""+EndCom)																
				elif id==54:
					#cpu total usage"
					ser.write("cpuusage.val="+replaceerro(valor)+""+EndCom)																		
				elif id==74:
					#gpu core"	                              
					ser.write("gpucore.txt=\""+code(valor)+"\""+EndCom)
				elif id==75:
					#gpumemory"	                              
					ser.write("gpumemory.txt=\""+code(valor)+"\""+EndCom)
				elif id==76:
					#gpu shader"	                              
					ser.write("gpushader.txt=\""+code(valor)+"\""+EndCom)
				elif id==78:
					#gpu core c"	                              
					ser.write("tempgpu.txt=\""+code(valor)+"\""+EndCom)
				elif id==80:
					#gpu core load"
					ser.write("gpucoreusage.val="+replaceerro(valor)+""+EndCom)
				elif id==81:
					#gpu core load"
					ser.write("gpucontrusage.val="+replaceerro(valor)+""+EndCom)
				elif id==82:
					#gpu core load"
					ser.write("gpuvideousage.val="+replaceerro(valor)+""+EndCom)
				elif id==83:
					#gpu core load"
					ser.write("gpumemusage.val="+replaceerro(valor)+""+EndCom)





# animacao leds
def colorWipe(strip, color,stop):
	while (True):
		"""Wipe color across display a pixel at a time."""
		for i in range(strip.numPixels()):        
			strip.setPixelColor(i, color)
			strip.show()
			time.sleep(0.05)
		if stop():            	
			break	

#tratamento erros do Hex
def tratamentoHex(args):
	if len(args) == 31:
		return int(args[4:-25],16) 		
	elif len(args) == 28: 
		return int(hex(ord(args[2:-25]))[2:],16) 

					
					

if __name__ == '__main__':
	gpio.setwarnings(False) #desativa mensagem de perigo gpio
	gpio.setmode(gpio.BOARD)

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
	
	
	
	try:		
		while(True):
			
			ser = iniciarSerial()	#chama funcao para iniciar serial
			ser.write('sendme'+EndCom) #verifica qual tela nextion esta
			numeroTela = code(repr(ser.readline())) #pega o numero da tela
			if 'x00' in numeroTela:		# se for na tela 00 preencher dados pc
				preenchertela()	
			elif 'x01' in numeroTela:
				ser.write('get page1.va0.txt'+EndCom) #se for na tela 01 pedir valor da variavel que contem o pwm
				pwmAtual= code(repr(ser.readline()))[2:-13] #pega valor somente do pwm			
				if pwmAtual != "x1a":					
					pwmAtual = int(pwmAtual)
					if pwmValue != pwmAtual: #se o pwm for diferente do atual seta novo pwm a thread
						pwmValue = pwmAtual	  #atribiu novo pwm
						stop_threads_pwm = True #atribui para thread
						pwm.join()          #para thread
						stop_threads_pwm = False #cancela parada thread
						pwm = threading.Thread(target=pwmSet,args=(pwmValue,lambda: stop_threads_pwm) ) #cria nova thread
						pwm.setDaemon(True)
						pwm.start()			   #inicia nova thread

			elif 'x02' in numeroTela:				
				ser.write('get page2.nRed.val'+EndCom) #valor led vermelha
				tempRed=tratamentoHex(repr(ser.readline())) #tratamento de excessao

				ser.write('get page2.nBlue.val'+EndCom) #valor led azul
				tempBlue=tratamentoHex(repr(ser.readline())) #tratamento de excessao		

				ser.write('get page2.nGreen.val'+EndCom) #valor led verde
				tempGreen=tratamentoHex(repr(ser.readline())) #tratamento de excessao
				if ledRed != tempRed or ledBlue != tempBlue or ledGreen != tempGreen: #tratamento de excessao
					teste = ""+str(tempRed)+str(tempBlue)+str(tempGreen) #tratamento de excessao
					if "x1a" not in teste: #tratamento de excessao
						ledRed=tempRed
						ledBlue=tempBlue
						ledGreen=tempGreen
						stop_threads_leds = True #True para parar Theread
						leds.join()
						stop_threads_leds = False #False para parar Theread
						leds = threading.Thread(target=colorWipe,args=(strip, Color(ledGreen,ledRed,ledBlue),lambda: stop_threads_leds) ) #cria nova thread
						leds.setDaemon(True)
						leds.start()
	
				
		
			

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
		