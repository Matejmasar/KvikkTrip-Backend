from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route('/location', methods=['GET', 'POST', 'PUT', 'DELETE'])
def location():
    if request.method == 'GET':
        return "List of locations"
    else:
        if request.method == 'POST':
            #add new location
            return "Added location"
        else:
            if request.method == 'PUT':
                #update location
                return "Updated location"
            else:
                if request.method == 'DELETE':
                    #Delete location
                    return "List of locations"



@app.route('/user', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user():
    if request.method == 'GET':
        return "List of users"
    else:
        if request.method == 'POST':
            #add new user
            return "Added user"
        else:
            if request.method == 'PUT':
                #update user
                return "Updated user"
            else:
                if request.method == 'DELETE':
                    #Delete user
                    return "List of users"


@app.route('/event', methods=['GET', 'POST', 'PUT', 'DELETE'])
def event():
    if request.method == 'GET':
        return "List of events"
    else:
        if request.method == 'POST':
            #add new event
            return "Added event"
        else:
            if request.method == 'PUT':
                #update event
                return "Updated event"
            else:
                if request.method == 'DELETE':
                    #Delete event
                    return "List of events"


@app.route('/tag', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tag():
    if request.method == 'GET':
        return "List of tags"
    else:
        if request.method == 'POST':
            #add new tag
            return "Added tag"
        else:
            if request.method == 'PUT':
                #update tag
                return "Updated tag"
            else:
                if request.method == 'DELETE':
                    #Delete tag
                    return "List of tags"