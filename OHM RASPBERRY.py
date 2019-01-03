#!/usr/bin/env python2
# coding: utf-8
import json
import requests
import urllib2
import time
import serial

url = ("http://192.168.2.235:8085/data.json") #url dados pc
EndCom = "\xff\xff\xff"

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
		dados = dados.encode('iso-8859-1').replace(','+str(i)+' %','')		
		i+=1
	return dados

def code(args):
	return args.encode('iso-8859-1')	

def preenchertela():	
		
		response = urllib2.urlopen(url) 
		jsond = json.loads(response.read())		 
		for dados in jsond:
			if 'Value' in json.dumps(jsond[dados['id']]):
				valor = dados['Value']
				id = dados['id']
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
					
while(True): 
	ser = iniciarSerial()			
 	preenchertela()					
