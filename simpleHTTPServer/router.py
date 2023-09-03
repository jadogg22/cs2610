import hTTP_Parser
import datetime
import response as responseClass


endpoints = {
'/': 'templates/index.html',
'/about': 'templates/about.html',
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
    print(f"here is the returned response: \n {response.classToResponseStr()}")
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
    response.locationHeader('/about')
    return response

def notFound(request):
    response_text = "404 Not Found"
    return responseClass.Response('HTTP/1.1', 404, 'Not Found', {'Content-Type': 'text/html'}, response_text)

# ----- middleware --------



def checkValidRoute(request):
    route = request.uri
    if route in endpoints:
        return endpoints[route]
    else:
        return False
        

def content_length(next):
    def middleware(response):
        response = next(response)
        response.setContent_length()
        return response
    return middleware

# def add_server_header(next):
#     def middleware(request):
#         response = next(request)
#         response.headers['Server'] = "Jaden\'s Server"
#         return response
#     return middleware

def add_date_header(next):
    def middleware(request):
        response = next(request)
        response.headers['Date'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return response
    return middleware

def add_connection_close(next):
    def middleware(request):
        response = next(request)
        response.headers['Connection'] = 'close'
        return response
    return middleware

def add_cashed_control(next):
    def middleware(request):
        response = next(request)
        response.headers['Cache-Control'] = '200'
        return response
    return middleware

def add_content_type(next):
    def middleware(res):
        response = next(res)
        response.headers['Content-Type'] = 'text/html'
        return response
    return middleware


# ----- router --------

def route(request):
    if request.method != 'GET':
        return notFound(request)
    if request.version != 'HTTP/1.1':
        return notFound(request)
    
    route = request.uri #get the path from the request
    if route in endpoints:
        if route == '/style.css':
            return responseClass.Response('HTTP/1.1', 200, 'OK', {'Content-Type': 'text/css'}, readFile('static/style.css'))
        elif route == '/script.js':
            return responseClass.Response('HTTP/1.1', 200, 'OK', {'Content-Type': 'text/javascript'}, readFile('static/code.js'))
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

