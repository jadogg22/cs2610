import request
import response

def decodeRequest(data):
    newData = str(data, "UTF-8")
    parsedData = parse_headers(newData)
    return parsedData

def parse_headers(headers_str):
    headers = {}
    header_lines = headers_str.split('\n')

    #Remove and parse request line
    request_line = header_lines.pop(0)
    parts = request_line.split()
    method = parts[0]
    uri = parts[1]
    version = parts[2]
    text = ""
    inHeader = True

    for line in header_lines:
        #check for the blank line that signifys end of headers
        if line.strip() == '':
            inHeader = False
            continue
        # if we are nolonger in the header, add the rest of the lines to the text
        if inHeader == False:
            text += f"{line}\n"
            continue

        header, value = line.split(':', 1)
        header = header.strip()
        value = value.strip()
        
        # Add header to dict
        headers[header] = value

    # create request class and return it
    parsedRequest = request.Request(method, uri, version, text, headers)

    return parsedRequest 

def encodeResponse(response):
    text = response.classToResponseStr()
    print(text)
    return bytes(text, "UTF-8")

debugResponse = response.Response('HTTP/1.1', 200, 'OK', {"date": "today"}, "Hello World")

#debugResponse.createServerHeader("Jaden\'s Server")
#print(debugResponse.classToResponseStr())