# server .py
1. start up server and wait for connection and request
2. parse request and create request object 

3. make response

send response 

## router.py

first middleware
    example GET / HTTP/1.1
    a. check if valid get request 
    b. check check valid path
        if ends with css or js
            special
        else call endpoint; returns response

secound middleware
    a. if code == 200 OR 301
        middlewarefactory(
            server
            date
            connection
            cache-control

            content-Length
            content-type
        )
        

