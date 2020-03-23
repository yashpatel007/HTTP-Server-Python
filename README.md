Project : Http Server
Server Description:</br>

        1. Server is a simple http server. This server can serve a file requested with appropriate headers, it also counts
           the number of acesses to the file.</br> 
        2. Server is running on the port : 8082</br>
        3. Server is a multithreaded server and can serve the request coming in parallel</br>
        
Compiling project:

        1.In order to compile the priject login to any remote server machine and navigate to the repository folder.</br>
        2.Once inside the folder type the command : <b>make</b>
        3. This should compile the file and start the server and you should be able to see 
               >> server started at HOSTNAME : remote07 on IP: 128.226.114.207  PORT : 8082
           in this case the server was started on remote07 and IP address and port number is also displayd
           
 Sending requests:
 
        1. log in to remote server from another console window and type wget http://remoteXX.cs.binghamton.edu:8082/index.html 
           and it will download the index.html into your cuttent folder
           
                 >> --2019-09-24 13:58:14--  http://remote07.cs.binghamton.edu:8082/index.html
                    Resolving remote07.cs.binghamton.edu (remote07.cs.binghamton.edu)... 128.226.114.207
                    Connecting to remote07.cs.binghamton.edu (remote07.cs.binghamton.edu)|128.226.114.207|:8082... connected.
                    HTTP request sent, awaiting response... 200 OK
                    Length: 181 [text/html]
                    Saving to: ‘index.html’
                    index.html               100%[==================================>]     181  --.-KB/s    in 0s
                    2019-09-24 13:58:14 (25.2 MB/s) - ‘index.html’ saved [181/181]
        
        2. To check the multi-threading parallel requestd can also be sent. using the curl command.   
