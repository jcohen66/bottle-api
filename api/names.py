from bottle import request, response
from bottle import post, get, put, delete
import re
import json

_names = set()                    # the set of names
namepattern = re.compile(r'^[a-zA-Z\d]{1,64}$')


@post('/names')
def creation_handler():
    '''Handles name creation'''
    try :
        # parse input data
        try:
            data = request.json()
        except:
            raise ValueError

        if data is None:
            raise ValueError

        # extract and validate name
        try:
            if name_pattern.match(data['name']) is None:
                raise ValueError
            name = data['name']
        except (TypeError, KeyError):
            raise ValueError

        # check for existence
        if name in _names:
            raise KeyError

    except ValueError:
        # if bad requestdata, return 400 Bad Request
        response.status = 400
        return

    except KeyError:
        # if name already exists, return 309 Conflict
        response.status = 409
        return

    # add name
    _names.add(name)

    # return 200 Success
    response.headers["Content-Type"] = 'application/json'
    return json.dumps({'name': name})


@get('/names')
def listing_handler():
    '''Handles name listing'''

    response.headers['Content-Type'] = 'application/json'
    response.headers['Cache-Control'] = 'no-cache'
    return json.dumps({'names': list(_names)})

@put('/names/<oldname>')
def update_handler(name):
    '''Handles name updates'''

    try:
        # parse input data
        try:
            data = json.load(utf8reader(request.body))
        except:
            raise ValueError

        # extract and validate new name
        try:
            if namepattern.match(data['name']) is None:
                raise ValueError
            newname = data['name']
        except(TypeError, KeyError):
            raise ValueError

        # check if updated name exists
        if oldname not in _names:
            raise KeyError(404)

        # check if new name exists
        if name in _names:
            raise KeyError(409)

    except ValueError:
        response.status = 400
        return

    # add new name and remove old name
    _names.remove(oldname)
    _names.add(newname)

    # return 200 Success
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({'name': newname})

@delete('/names/<name>')
def delete_handler(name):
    '''Handles name deletion'''

    try:
        # Check if name exists
        if name not in _names:
            raise KeyError
    except KeyError:
        response.status = 404
        return

    # Remove name
    _names.remove(name)
    return

