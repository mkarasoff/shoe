##########################################################################
#SHOE - An open source HEOS configuration and control project
#Copyright (C) 2020  Mike Karasoff, mike@karatronics.com
#
#toeJam.py
#A bunch of independent commands used to quickly "jam" commands and
#responses between HEOS and host controller.  This is a standalone
#tool used for proof of concept.
#
#
##########################################################################
#GPLv.3 License
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################
import http.client, urllib.request, urllib.parse, urllib.error
from http.client import HTTPConnection
from datetime import datetime
import time

#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#params = ""
#conn.request()
#res = conn.getresponse()
#time.sleep(1)

#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#now=datetime.utcnow()
#gmttime = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
#conn.putrequest('GET', '/upnp/desc/aios_device/aios_device.xml', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('DATE', gmttime)
#conn.putheader('CONNECTION', 'close')
#conn.putheader('USER-AGENT' , 'LINUX UPnP/1.0 Denon-Heos/149200')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()

#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/renderer_dvc/ConnectionManager', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/renderer_dvc/AVTransport', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/renderer_dvc/RenderingControl', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/AiosServicesDvc/GroupControl', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/AiosServicesDvc/ErrorHandler', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/upnp/event/AiosServicesDvc/ZoneControl', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)
#conn = httplib.HTTPConnection("10.42.12.12", 60006)
#conn.set_debuglevel(100000)
#conn.putrequest('SUBSCRIBE', '/ACT/event', skip_accept_encoding=True)
#conn.putheader('HOST', '10.42.12.12:60006')
#conn.putheader('CALLBACK', '<http://10.42.12.143:49200/>')
#conn.putheader('NT', 'upnp:event')
#conn.putheader('TIMEOUT' , 'Second-180')
#conn.endheaders()
#res = conn.getresponse()
#conn.close()
#
#time.sleep(.5)

conn = http.client.HTTPConnection("10.42.12.12", 60006)
conn.set_debuglevel(100000)

params='''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:GetActiveInterface xmlns:u="urn:schemas-denon-com:service:ACT:1"></u:GetActiveInterface></s:Body></s:Envelope>'''
msg_len=str(len(params))
conn.putrequest('POST', '/ACT/control', skip_accept_encoding=True)

conn.putheader('CONTENT-LENGTH', msg_len)
conn.putheader('HOST', '10.42.12.12:60006')
conn.putheader('Accept-Ranges', 'bytes')
conn.putheader('CONTENT-TYPE' , 'text/xml; charset="utf-8"')
conn.putheader('SOAPACTION' , '"urn:schemas-denon-com:service:ACT:1#GetActiveInterface"')
conn.putheader('USER-AGENT' , 'LINUX UPnP/1.0 Denon-Heos/149200')

conn.endheaders(params)
res = conn.getresponse()
conn.close()

params='''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:GetConfigurationToken xmlns:u="urn:schemas-denon-com:service:ACT:1"></u:GetConfigurationToken></s:Body></s:Envelope>'''
msg_len=str(len(params))
conn.putrequest('POST', '/ACT/control', skip_accept_encoding=True)

conn.putheader('CONTENT-LENGTH', msg_len)
conn.putheader('HOST', '10.42.12.12:60006')
conn.putheader('Accept-Ranges', 'bytes')
conn.putheader('CONTENT-TYPE' , 'text/xml; charset="utf-8"')
conn.putheader('SOAPACTION' , '"urn:schemas-denon-com:service:ACT:1#GetConfigurationToken"')
conn.putheader('USER-AGENT' , 'LINUX UPnP/1.0 Denon-Heos/149200')

conn.endheaders(params)
res = conn.getresponse()
conn.close()
