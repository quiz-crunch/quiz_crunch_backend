import json


class ApiResponse:
    def __init__(self, code=200, message=None, data=None, ):
        self.code = code
        self.message = message
        self.data = data

    def to_json(self):
        return {
            "code": self.code,
            "message": self.message,
            "data": self.data
        }
