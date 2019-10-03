from flask import request
from flask_appbuilder.api import BaseApi, expose, rison, safe
from . import appbuilder
import prison


class ExampleApi(BaseApi):
    '''Api with format http://host:port+'/api/v1/'+class_name_in_small+@expose'''
    #to change default class_name_in_small url to custome url
    resource_name = 'example'
    #base_route = '/newapi/v2/nice'

    schema = {
        "type": "object",
        "properties": {
            "name": {
                "type": "string"
            }
        }
    }
    
    print(prison.dumps(schema))

    @expose('/greeting/')
    def greeting(self):
        return self.response(200, message="Hello")

    @expose('/greeting2', methods=['POST', 'GET'])
    def greeting2(self):
        if request.method == 'GET':
            return self.response(200, message="Hello (GET)")
        return self.response(201, message="Hello (POST)")

    @expose('/greeting3')
    @rison()
    def greeting3(self, **kwargs):
        if 'name' in kwargs['rison']:
            return self.response(
                200,
                message="Hello {}".format(kwargs['rison']['name'])
            )
        return self.response_400(message="Please send your name")

    @expose('/risonjson')
    @rison()
    def rison_json(self, **kwargs):
        return self.response(200, result=kwargs['rison'])

    @expose('/greeting4')
    @rison(schema)
    def greeting4(self, **kwargs):
        print('''
        
        ----
        
        ''',kwargs.items())
        return self.response(
            200,
            message="Hello {}".format(kwargs['rison']['properties']['name'])
        )
    
    @expose('/error')
    @safe
    def error(self):
        raise Exception


print('''

apis created

''')
appbuilder.add_api(ExampleApi)