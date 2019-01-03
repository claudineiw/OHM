#!/usr/bin/env python2
# coding: utf-8
import json
import requests
import urllib2
import time
import serial



def replaceerro(args):
		return args.encode('iso-8859-1').replace(',1 %','').replace(',2 %','').replace(',3 %','').replace(',4 %','').replace(',5 %','').replace(',6 %','').replace(',7 %','').replace(',8 %','').replace(',9 %','').replace(',0 %','')
			



ser = serial.Serial(
  port='/dev/ttyS0',
  baudrate = 9600,
  parity=serial.PARITY_NONE,
  stopbits=serial.STOPBITS_ONE,
  bytesize=serial.EIGHTBITS,
  timeout=1
)

EndCom = "\xff\xff\xff"
url = ("http://192.168.2.235:8085/data.json")

while(True):
        
	
	response = urllib2.urlopen(url) 
	jsond = json.loads(response.read())		 
	for dados in jsond:
		if 'Value' in json.dumps(jsond[dados['id']]):
		                if dados['id']==28:
					#WaterCooler rpm                            
					ser.write("waterrpm.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==39:
					#CPU Core #1"	                              
					ser.write("cpucore1.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==40:
					#CPU Core #2"	                              
					ser.write("cpucore2.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==41:
					#CPU Core #3"	                              
					ser.write("cpucore3.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==42:
					#CPU Core #4"	                              
					ser.write("cpucore4.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==43:
					#CPU Core #5"	                              
					ser.write("cpucore5.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==44:
					#CPU Core #6"	                              
					ser.write("cpucore6.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==52:
					#cpu package 36 C"	                              
					ser.write("cputemp.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==54:
					#cpu total usage"
					ser.write("cpuusage.val="+replaceerro(dados['Value'])+""+EndCom)
				if dados['id']==74:
					#gpu core"	                              
					ser.write("gpucore.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==75:
					#gpumemory"	                              
					ser.write("gpumemory.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==76:
					#gpu shader"	                              
					ser.write("gpushader.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==78:
					#gpu core c"	                              
					ser.write("tempgpu.txt=\""+dados['Value'].encode('iso-8859-1')+"\""+EndCom)
				if dados['id']==80:
					#gpu core load"
					ser.write("gpucoreusage.val="+replaceerro(dados['Value'])+""+EndCom)
				if dados['id']==81:
					#gpu core load"
					ser.write("gpucontrusage.val="+replaceerro(dados['Value'])+""+EndCom)
				if dados['id']==82:
					#gpu core load"
					ser.write("gpuvideousage.val="+replaceerro(dados['Value'])+""+EndCom)
				if dados['id']==83:
					#gpu core load"
					ser.write("gpumemusage.val="+replaceerro(dados['Value'])+""+EndCom)
				


					
		#else:
			#print dados['id']
			#print dados['Text']

	
	