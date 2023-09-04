import hTTP_Parser
import datetime
import response as responseClass


endpoints = {
'/': 'templates/index.html',
'/about': 'templates/about.html',
'/info': 'templates/about.html',
'/experience': 'templates/experience.html',
'/projects': 'templates/projects.html',
'/style.css': 'static/style.css',
'/script.js': 'static/code.js'
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
    response.headers['Content-Type'] = 'text/html'
    response.headers['Date'] = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    response.headers['Server'] = 'Jaden\'s Server'
    response.headers['Connection'] = 'close'
    response.headers['Last-Modified'] = 'Wed, 21 Oct 2015 07:28:00 GMT'
    response.headers['Content-Length'] = len(response.classToResponseStr())


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
        

# ----- middleware --------



def checkValidRoute(request):
    route = request.uri
    if route in endpoints:
        return endpoints[route]
    else:
        return False

def add_content_type(next):
    def middleware(res):
        response = next(res)
        response.headers['Content-Type'] = 'text/html'
        return response
    return middleware


# ----- router --------

def route(request):
    
 
    route = request.uri #get the path from the request
    if route.endswith('.js'):
        return scriptJS(request)
    if route.endswith('.css'):
        return styleCSS(request)
    
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

    return notFound(request)

def route2(request):

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
            
    else:
        return notFound(request)

    return notFound(request)


def middleWare_Static_files(next):

    def middleware(request):
        if request.uri.endswith('.js'):
            return scriptJS(request)
        if request.uri.endswith('.css'):
            return styleCSS(request)
        #if not a static file then return the route
        return next(request)
    return middleware

def middleware_Log(next):
    def middleware(request):
        print(f"{request.method} {request.uri} HTTP/1.1")
        return next(request)
    return middleware

def routeFractory(request):
    middleware = middleWare_Static_files(route)
    return middleware(request)

def compose(end_handler, middleware_list):
    
    # Start with end handler
    previous_handler = end_handler
    
    # Loop in reverse through middleware
    for middleware in reversed(middleware_list):
      
        # Nest previous handler inside current middleware 
        previous_handler = middleware(previous_handler)
    
    # Return composed function chain
    return previous_handler



