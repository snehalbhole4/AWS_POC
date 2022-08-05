import json
from decimal import Decimal

class CustomeEncoder(json.JSONEncoder):
    def default(self,obj):
        if isinstance(obj,Decimal):
            return float(obj)

        return json.JSONEncoder.default(self,obj)

body = {
            'Operation': 'DELETE',
            'Message':'SUCCESS',
    
        }
