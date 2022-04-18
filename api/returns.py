from flask import Flask
import json


def return_json(object, code=200):
    response = Flask.response_class(
        response=json.dumps(object),
        status=code,
        mimetype="application/json"
    )
    return response


def return_error(message, code=400):
    error = {"message": message}

    return return_json(error, code)
