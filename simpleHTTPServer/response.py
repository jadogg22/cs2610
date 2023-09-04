class Response:
    def __init__(
            self,
            version, #string
            code, #number
            reason, #string
            headers, #dict, the keys are the header names and values are the header values 
            text, #string
    ):
        self.version = version
        self.code = code
        self.reason = reason
        self.headers = headers
        self.text = text

    #prints the entire response object 
    def classToResponseStr(self):
        text = ""
        text += f"{self.version} {self.code} {self.reason}\n"
        for header in self.headers:
            text += f"{header}: {self.headers[header]}\n"
        text += "\n"    
        text += f"{self.text}"
        return text
    
    #print(text)
    def __repr__(self):
        return "Response: " + self.version + " " + str(self.code) + " " + self.reason + "\n"
    
    def getContent_length(self):
        return len(bytes(self.text, "UTF-8"))
        
