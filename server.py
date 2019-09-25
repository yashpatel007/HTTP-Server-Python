import socket
import datetime
import os
import os.path
import time
import stat
import magic

# import thread module 
from _thread import *
import threading

#arrays to keep track of number of access for the file
myfiles =[]
myaccess =[]

def getaccesses(filename):
    for i in range (len(myfiles)):
        if(filename == myfiles[i]):
            idx = i
    return myaccess[idx]


def addfile(filename):
    if(filename in myfiles):
        for i in range(len(myfiles)):
            if(filename == myfiles[i]):
                idx=i
        myaccess[idx] = myaccess[idx]+1 
    else:
        myfiles.append(filename)
        myaccess.append(1)
    return 0


print_lock = threading.Lock() 
  
# thread fuction 
def threaded(connection,address):

	#print (threading.currentThread().getName(), 'Starting','\n')
    
    	# maximum 1024 bytes requested over here
	req = connection.recv(1024)
	req = req.decode('utf-8')
	
    	#print("\n\n\n")
    	#print ('**************** REQUEST HEADERS ********************')
    	#print(req) # Get print in our python console
    	#print ('*****************************************************')
	
	file_name = "www" #file to be searched
	cur_dir = os.getcwd() # Dir from where search starts can be replaced with any path
	file_list = os.listdir(cur_dir)
	parent_dir = os.path.dirname(cur_dir)
    	#print(len(req))
	
	#this condition is to handle the empty headers if requested
	if (len(req)!=0):
		#check if the file www exist in the current repo or not
		if file_name in file_list:
			
            		#print ("File Exists\n")
			
			string_list = req.split(' ')# Split request from spaces
			method = string_list[0] # First string is a method
			requesting_file = string_list[1] #Second string is request file
			
            		#print('Client request ',requesting_file)

			myfile = requesting_file.split('?')[0] # After the "?" symbol not relevent here
			myfile = myfile.lstrip('/')
			
			#so my file is now either the file we input or an empty file as index.html
            		#print(myfile)

			v = addfile(myfile)
            		#print(myfiles)
            		#print(myaccess)
			
			try:
				file = open('./www/'+myfile,'rb') # open file , r => read , b => byte format
				response = file.read()
				file.close()
				
				#print(response)
				
				header = 'HTTP/1.1 200 OK\n'

				mime = magic.Magic(mime=True)
				mimetype = mime.from_file("./www/"+myfile)

				#add contents to the responce headers

				#getting date and time
				date = time.asctime( time.gmtime(time.time()) )
				#getting last modified time
				statbuf = os.stat('./www/'+myfile)
				modificationtime = time.asctime ( time.gmtime(statbuf [ stat.ST_MTIME ] ))
				#get the size of tee file
				filesize = os.stat('./www/'+myfile).st_size

				#server host name
				hostname = socket.gethostname()

				#prepare the header responce
				header += 'Content-Type: '+str(mimetype)+'\n'+'Date:'+str(date)+'\n'+'Last Modified:'+str(modificationtime)+'\n'+'Server:'+str(hostname)+'\n'+'Content-Length:'+str(filesize)+'\n\n'


			except Exception as e:
				header = 'HTTP/1.1 404 Not Found\n\n'
				response = '<html><body><center><h3>Error 404: File not found</h3><p>Python HTTP Server</p></center></body></html>'.encode('utf-8')
			
			# info og the client it is connected to
			print('/',myfile,' | ', address[0], ' | ', address[1],' | ', getaccesses(myfile))
			final_response = header.encode('utf-8')
			final_response += response
			#print("*************** RESPONCE HEADER *******************")
			#print(header)
			#print('***************************************************')
			connection.send(final_response)

		else:
			print("error: WWW not found...(exiting)")
			exit()
	else:
		print('No Request Headers')

	connection.close()
	#print("BYE")
	print_lock.release()
	#print (threading.currentThread().getName(), 'Exiting','\n')



def Main():
	HOST, PORT = '',8082
	#sockstream use the tcp protocol
	mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	mysocket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
	mysocket.bind((HOST,PORT))
	mysocket.listen(1)
	print("server started at HOSTNAME :",socket.gethostname(),"on IP:",socket.gethostbyname(socket.gethostname())," PORT :",PORT)
	while True:

		connection,address = mysocket.accept()
		# lock acquired by client 
		print_lock.acquire()
		start_new_thread(threaded, (connection,address))

	mysocket.close()



if __name__ == '__main__': 
	Main()
	




