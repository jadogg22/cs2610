import socket
import hTTP_Parser
import router
import test


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("127.0.0.1", 8000))
    s.listen()
    print("listening on port 8000")

    while True:
        connection, addr = s.accept()
        with connection:
            data = connection.recv(8192)
            if not data:
                connection.close()
                continue
            
            
            request = hTTP_Parser.decodeRequest(data) # returns a request object 

            response = test.createResponse(request)
            


            #TODO: parse the request, send through middleware and encode the response
            #res = "HTTP/1.1 200 Ok\nConnection: close\n\n<h1>Hello, world!</h1>"
            
            encodedText = hTTP_Parser.encodeResponse(response)

            connection.send(encodedText)
            connection.close()