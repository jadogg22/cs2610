import datetime
import response as responseClass
import request as requ


endpoints = {
'/': 'templates/index.html',
'/about': 'templates/about.html',
'/info': 'templates/about.html',
'/experience': 'templates/experience.html',
'/projects': 'templates/projects.html',
}

#------endpoints---------

def readFile(file):
    with open(file, 'rb') as f:
        content = str(f.read(), "UTF-8")
    return content

def projects(request):
    response_text = readFile('templates/projects.html')
    return responseClass.Response('HTTP/1.1', 200, 'OK', {}, response_text)

def index(request):
    response_text = readFile('templates/index.html')
    response = responseClass.Response('HTTP/1.1', 200, 'OK', {}, response_text)
    return response

def about(request):
    response_text = readFile('templates/about.html')
    return responseClass.Response('HTTP/1.1', 200, 'OK', {}, response_text)

def experience(request):
    response_text = readFile('templates/experience.html')
    return responseClass.Response('HTTP/1.1', 200, 'OK', {'Content-Type': 'text/html'}, response_text)

def info(request):
    response = responseClass.Response('HTTP/1.1', 301, 'OK', {}, '')
    response.headers['Location'] = '/about'
    return response

def notFound(request):
    response_text = f'{request.method} {request.uri} HTTP/1.1 404 Not Found\n\n<h1>404 Not Found</h1>'
    return responseClass.Response('HTTP/1.1', 404, 'Not Found', {'Content-Type': 'text/html'}, response_text)

def styleCSS(request):
    response_text = readFile('static/styles.css')
    response = responseClass.Response('HTTP/1.1', 200, 'OK', {'Content-Type': 'text/css'}, response_text)
    response.headers['Content-Length'] = response.getContent_length()
    return response

def scriptJS(request):
    response_text = readFile('static/code.js')
    response = responseClass.Response('HTTP/1.1', 200, 'OK', {'Content-Type': 'text/javascript'}, response_text)
    response.headers['Content-Length'] = response.getContent_length()
    return response
        

# ----- middleware --------
def neededHeaders_middleware():
    def middleware(response):
        response.headers['Content-Type'] = 'text/html'
        response.headers['Server'] = 'Jaden\'s Server'
        response.headers['Connection'] = 'close'
        response.headers['Cache-Control'] = 'max-age=200'
        response.headers['Date'] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

        return response
    return middleware


def contentLength_middleware():
    def middleware(response):
        if response.code not in [404, 401, 301, 418]:
            response.headers['Content-Length'] = response.getContent_length()
        return response
    return middleware


# ----- router --------response


def middleWare_logging():
    def middleware(object):
        if isinstance(object, requ.Request):
            print(f'request: {object.method} {object.uri}')
        elif isinstance(object, responseClass.Response):
            #TODO: add logging for response uri
            print(f'responese: {object.code} {object.reason}')
        return object
    return middleware

def middleWare_Static_files():
    def middleware(request):
        if request.uri.endswith('.js'):
            return scriptJS(request)
        if request.uri.endswith('.css'):
            return styleCSS(request)
        #if not a static file then return the route
        return request
    return middleware
    
def checkValidRoute():
    def middleware(request):
        if isinstance(request, responseClass.Response):
            return request
        
        route = request.uri
        if route in endpoints:
            if route == '/':
                return index(request)
            elif route == '/about':
                return about(request)
            elif route == '/experience':
                return experience(request)
            elif route == '/projects':
                return projects(request)
            elif route == '/info':
                return info(request)
                    
        else:
            return notFound(request)
        
    return middleware

#request = hTTP_Parser.parse_headers('GET / HTTP/1.1\nHost: localhost.8000\nConnection: keep-alive\nCache-Control: max-age=0\nUpgrade-Insecure-Requests: 1\nUser-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko)\nChrome/91.0.4472.114 Safari/537.36\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng\nAccept-Encoding: gzip, deflate, br\nAccept-Language: en-US,en;q=0.9\n\n')
# middleware chain is reverse order
def createResponse(request):
    response =  middleWare_logging()(
                checkValidRoute()(
                middleWare_Static_files()(
                middleWare_logging()(request))))
    
    #for the additional headers
    if request.uri in endpoints:
        response =  contentLength_middleware()(
                    neededHeaders_middleware()(response))

        
    return response
            
request = requ.Request("GET", "/", "HTTP/1.1",'',{})
response = createResponse(request)