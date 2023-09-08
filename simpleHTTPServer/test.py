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
    response_text = readFile('templates/about.html')
    response = responseClass.Response('HTTP/1.1', 301, 'OK', {'Content-Type': 'text/html'}, response_text)
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
        

# ----- helper functions --------
def addneededHeaders(response):
    if isinstance(response, responseClass.Response):
        
        if response.code not in [404, 401, 418]:

            response.headers['Server'] = 'Jaden\'s Server'
            response.headers['Connection'] = 'close'
            response.headers['Cache-Control'] = 'max-age=200'
            response.headers['Date'] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")

    
    return response


def addcontentLength(response):
        if isinstance(response, responseClass.Response):
            
            if response.code not in [404, 401, 301, 418]:
                response.headers['Content-Length'] = response.getContent_length()
                return response
            
        return response
        


#----- middleware --------

def middleWare_logging(next):
    def middleware(request):
        print(f'Request: {request.method} {request.uri}')
        response = next(request)
        print(f'Response: {request.uri} {response.code} {response.reason}\n')
        return response
    return middleware

def middleWare_Static_files(next):
    def middleware(request):
        if request.uri.endswith('.js'):
            return scriptJS(request)
        if request.uri.endswith('.css'):
            return styleCSS(request)
        #if not a static file then return the route
        return next(request)
    return middleware
    

# ----- router --------    
def router(request):
    if isinstance(request, responseClass.Response): #it is a response object, not a request thus do not route
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

def compose(router_func, middleware_list):

  def composed(request):
    
    next = router_func
    
    for middleware in (middleware_list):
      next = middleware(next)

    return next(request)

  return composed

def createResponse(request):

    middleware_chain = compose(router, [middleWare_logging, middleWare_Static_files])


    response = middleware_chain(request)
    response = addcontentLength(response)
    response = addneededHeaders(response)


    return response


            