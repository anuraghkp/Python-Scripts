import sys
import socket
import threading

# Globel Varible for proxy.....
loc_target=""
loc_port=0
rem_target=""
rem_port=0

# help and uage.........
def usage():
	
	print "Simple Proxy"
	print 
	print "Developed By Anuragh"
	print "Usage : proxy.py  -lhost localhost -lport localport -rhost remotehost -rport remoteport"
	print 
	print "-h --help"
def main():

