import json
import requests

class PlaceHolderClient: 
    def get_something(self):
        request = requests.get("https://jsonplaceholder.typicode.com/todos/1")
        print("get something: ")
        print("status code response: ", request.status_code)
        print("content response: ", request.content)
        all_fields = json.loads(request.content)
        print(all_fields)
        
        
    def delete_something(self):
        request = requests.delete("https://jsonplaceholder.typicode.com/todos/1")
        print("delete something: ")
        print(request.status_code)


    def post_something(self):
        json = {
            'title':'foo',
            'body': 'test',
            'userId': 1
        }
        headers = {'Referer': 'http://en.wikipedia.org/wiki/Main_Page'}
        request = requests.post("https://jsonplaceholder.typicode.com/todos", json, headers=headers)
        print("post something: ")
        result_header = request.headers['Content-Type'] #Referer']
        print("result_header: ", result_header)
        for name in request.headers:
            print('header.name:', name, ' - header.value:', request.headers[name])
        print("status code response: ", request.status_code)
        print("content response: ", request.content)


    def update_something(self):
        json = {
            'title':'foo',
            'body': 'test 2',
            'userId': 1
        }
        request = requests.put("https://jsonplaceholder.typicode.com/todos/1", json)
        print("update something: ")
        print("status code response: ", request.status_code)
        print("content response: ", request.content)    