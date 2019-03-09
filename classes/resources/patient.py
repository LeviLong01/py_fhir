import os
import sys
from flask import request
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../queries'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../schemas'))

from patient_queries import PatientQueries
from patient_schema import PatientSchema
from patient_db import PatientDatabase
patient_queries = PatientQueries()
patient_schema = PatientSchema()
patient_db = PatientDatabase()


def to_json(data, http_code):
    headers = {
        'Content-Type': 'application/json'
    }
    return json.dumps(data), http_code, headers


class Patient:
    def __init__(self):
        return

    def patient(self):
        if request.method == 'GET':
            # Get by logical ID
            if request.args.get('_id'):
                return patient_queries.query_logical_id()
            # Get by system identifier ()
            elif request.args.get('identifier'):
                return patient_queries.query_identifier()
            # Get by gender
            elif request.args.get('gender'):
                # Get by gender limit results returned
                if request.args.get('_count'):
                    count = request.args.get('_count')
                    return patient_queries.query_gender(count)
                else:
                    count = -1
                    return patient_queries.query_gender(count)
            # Get by given name
            elif request.args.get('given') or request.args.get('given:contains') or request.args.get('given:exact'):
                return patient_queries.query_given_name()
            # Get by family name
            elif request.args.get('family') or request.args.get('family:contains') or request.args.get('family:exact'):
                return patient_queries.query_family_name()
            # Unable to recognize query
            else:
                error = {'resourceType': 'OperationOutcome',
                         'issue': [{
                             'severity': 'error',
                             'code': 'invalid',
                             'details': {
                                 'text': 'Query not recognized'
                             }
                         }]}
                return to_json(error, 400)

        # Decide where to create logical ID (UUID)
        elif request.method == 'POST':
            # POST user info
            request_data = request.get_json()
            json_data = patient_schema.get_schema(request_data)
            patient_db.insert_new_patient(json_data)
            return to_json(json_data, 200)

        elif request.method == 'PUT':
            # PUT user info
            request_data = request.get_json()
            json_data = patient_schema.get_schema(request_data)
            return to_json(json_data, 200)
        # Should never make it to below because app.py should return a 405 if method isn't in list
        else:
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': 'Method type ' + request.method + ' not supported'
                         }
                     }]}
            return to_json(error, 405)

    def patient_logical(self, logical_id):
        if request.method == 'GET':
            # Get by direct logical ID
            return patient_queries.query_logical_id_direct(logical_id)
        else:
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': 'Query not recognized'
                         }
                     }]}
            return to_json(error, 400)
