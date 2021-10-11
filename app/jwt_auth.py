import jwt

class JwtAuth():
    def __init__(self):
        self.key = "secret_key_goes_here"
    
    def encode(self, dic):
        encoded = jwt.encode(dic, self.key, algorithm="HS256")
        print(encoded)

        return encoded

    def decode(self, token):
        decoded = jwt.decode(token, self.key, algorithms=["HS256"])
        print(decoded)

        return decoded
