from flask import Blueprint, render_template, request, session
import json

lab6 = Blueprint('lab6', __name__)


offices = []
for i in range(1, 11):
    offices.append({
        "number": i,           
        "tenant": "",          
        "price": 900 + i * 100 
    })

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')


@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():

    data = request.json
    
    method = data.get('method')
    request_id = data.get('id')
    
    if method == 'info':
        return {
            "jsonrpc": "2.0",
            "result": offices,
            "id": request_id
        }
    
    elif method == 'booking':

        login = session.get('login')
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 1,  
                    "message": "Unauthorized"
                },
                "id": request_id
            }

        office_number = data.get('params')
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 2, 
                            "message": "Office already booked"
                        },
                        "id": request_id
                    }
                
                office['tenant'] = login
                return {
                    "jsonrpc": "2.0",
                    "result": "success",
                    "id": request_id
                }
    
    elif method == 'cancellation':
        login = session.get('login')
        if not login:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": 1,
                    "message": "Unauthorized"
                },
                "id": request_id
            }
        
        office_number = data.get('params')
        
        for office in offices:
            if office['number'] == office_number:
                if office['tenant'] != login:
                    return {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": 3,  
                            "message": "Cannot cancel other user's booking"
                        },
                        "id": request_id
                    }
                
                office['tenant'] = ""
                return {
                    "jsonrpc": "2.0",
                    "result": "success",
                    "id": request_id
                }
    
    return {
        "jsonrpc": "2.0",
        "error": {
            "code": -32601,
            "message": "Method not found"
        },
        "id": request_id
    }