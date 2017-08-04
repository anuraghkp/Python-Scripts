import sys
import socket
import getopt
import threading
import subprocess

#Globel varible

listen=False
command=False
upload=False
execute=""
target=""
upload_destination=""
port =0

# usage  function to usage details

def usage():
	print "Anuragh Net Tool"
	print
	print "Usage : netcat.py -t target_host  -p port"
	print "-l --listen"
	print "-e --execute=file_to_run "
	print "-c --command "
	print "-u upload destination"
	print 
	print
	print
	
def client_sender(buffer):
		client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		try:
			client.connect((target,port))
			if len(buffer):
				client.send(buffer)
			while True:
				recv_line=1
				responce=""
				while recv_line:
					data=client.recv(4096)
					recv_line=len(data)
					responce+=data
					if recv_line <4096 :
						break
				print responce
				buffer=raw_input("")
				buffer+="\n"
				client.send(buffer)
		except:
			print "[*] Eception Exiting."
			#down the connection
			client.close()
			
def server_loop():
	global target
	target="127.0.0.1"
	global port
	# if taarget is not defined listen on any client
	if not len(target):
		target="0:0:0:0"
	server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	server.bind((target,port))
	server.listen(5)
	while True:
		client_socket, addr=server.accept()
		client_thread=threading.Thread(target=client_handler,args=(client_socket,))
		client_thread.start()
def run_command(command):
	#trim the new line
	command=command.rstrip()
	try:
		output=subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
	except:
		output="Faild to execute command. \r \n"
	return output
def client_handler(client_socket):
	global upload
	global execute
	global command
	#check for file uplaod
	if len(upload_destination):
		#read  in all of the byte and write to ur destination
		file_buffer=""
		#keep reading data untile none is available
		while True:
			data=client_socket.recv(1024)
			if not data:
				break
			else:
				file_buffer+=data
		#now take byte and write them out
		try:
			file_decriptor=open(upload_destination,"wb")
			file_descriptor.write(file_buffer)
			file_descriptor.close()
			#ack that we wrote the file out
			client_socket.send("Successfully saved file to  %s\r\n" % upload_destination)
		except:
			client_socket.send("Faild to Uplaod");
	if len(execute):
		out=run_command(execute)
		client_socket.send(out)
	if command:
		while True:
			#show simple prompt
			client_socket.send("<Anuragh:#>")
				#now we see untile we see a linefeed
				#(enter key)
			cmd_buffer=""
			while "\n" not in cmd_buffer:
				cmd_buffer+=client_socket.recv(1024)
			responce=run_command(cmd_buffer)
			client_socket.send(responce)

# main function hande net cat..........

def main():
	global listen
	global target
	global  execute
	global command
	global uplaod_destination
	global port

	if not len(sys.argv[1:]):
		usage()
	try:
		opts, argv =getopt.getopt(sys.argv[1:],"hle:t:p:cu",["help","listen","execute","target","port","command","upload"])
	except getopt.GetoptError as err:
		print str(err);
		usage()
	for o,a in opts:
		print o
		if(o in ("-h","--help")):
			usage()
		elif(o in ("-l","--listen")):
			listen=True
		elif(o in ("-e","--execute")):
			execute=a;
		elif(o in ("-c","--command")):
			command=True
		elif(o in ("-u","--upload")):
			upload_destination=a
		elif(o in ("-t","--target")):
			target=a
		elif(o in ("-p","--port")):
			port=int(a)
		else:
			assert False, "Unhandled Option"

# check we are goint to listen or just send data
	if not listen and len(target) and port >0:
		#read in the buffer  from  the command  line
		#this will block,so send Ctrl+D  if not sending input to stdin
		buffer =sys.stdin.read()
		#send data off
		client_sender(buffer)
	# if we are going to listen and potentially
	#upload things, execute commands ,drop shell back depanding on our command line option above 
	if listen:
		server_loop()
main()
