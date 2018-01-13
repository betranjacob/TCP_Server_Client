# TCP_Server_Client
A simple TCP server client

# Server 
Waits in a loop for any client requets and creats separate threads for every responses. 
Returns integer response of executing “cmd” against the target at “address”. The server responds to requests by using the data in the supplied file. Each line follows the same format: <address>:<cmd to execute (always “foo” or “bar”)>:<response integer>:<wait>	 The “wait” field tells the server how many seconds to wait after receiving a request before responding (this simulates network delays and slow commands). We don’t want one request to be blocked because the server is waiting due to another one though, so you’ll have to make sure your server can handle concurrent requests. 
 
# Client 
This process should execute Cmd requests to the server twice for each IP address in the range 137.72.95.*, requesting the commands “foo” and “bar” (in either order). The client should calculate the total of all response integers received and output just this. We would like the client to complete in no more than a few seconds. The method of communication between the two processes is using TCP sockets.

