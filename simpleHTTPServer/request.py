class Request:
    def __init__(
        self,
        method, #string
        uri, #string
        version, #string
        text, #string
        headers, #dict, the keys are the header names and values are the header values
    ):
        self.method = method
        self.uri = uri
        self.version = version
        self.text = text
        self.headers = headers

    def __repr__(self):
        return "Request: " + self.method + " " + self.uri + " " + self.version+ "\n"
    
    def classToRequestStr(self):
        text = ""
        text += f"{self.method} {self.uri} {self.version}\n"
        for header in self.headers:
            text += f"{header}: {self.headers[header]}\n"
        text += "\n"    
        text += f"{self.text}"
        return text