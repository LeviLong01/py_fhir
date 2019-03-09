import os
import sys
from flask import Flask
from flask import render_template
import json

sys.path.append(os.path.join(os.path.dirname(__file__), './classes/resources'))

from patient import Patient
from relatedperson import RelatedPerson
patient = Patient()
relatedperson = RelatedPerson()


def to_json(data, http_code):
    headers = {
        'Content-Type': 'application/json'
    }
    return json.dumps(data), http_code, headers


app = Flask(__name__)


# Takes to main page for conformance statement
@app.route('/fhir/stu3/', methods=['GET'])
def get_main():
    return render_template('index.html')


# Routes by resource name and query parameters
@app.route("/fhir/stu3/<string:resource>", methods=['GET', 'POST', 'PUT'])
def request_resource(resource):
    if resource == 'patient':
        return patient.patient()
    elif resource == 'relatedperson':
        return relatedperson.relatedperson()
    else:
        error = {'resourceType': 'OperationOutcome',
                 'issue': [{
                     'severity': 'error',
                     'code': 'invalid',
                     'details': {
                         'text': 'Invalid resource.'
                     }
                 }]}
        return to_json(error, 400)


# Routes directly by a logical ID associated with a resource
@app.route("/fhir/stu3/<string:resource>/<string:logical_id>", methods=['GET', 'PUT'])
def request_logical_id(resource, logical_id):
    if resource == 'patient':
        return patient.patient_logical(logical_id)
    elif resource == 'relatedperson':
        return relatedperson.relatedperson_logical()
    else:
        error = {'resourceType': 'OperationOutcome',
                 'issue': [{
                     'severity': 'error',
                     'code': 'invalid',
                     'details': {
                         'text': 'Invalid resource.'
                     }
                 }]}
        return to_json(error, 400)


if __name__ == '__main__':
    app.run()
