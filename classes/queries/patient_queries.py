import os
import sys
from flask import request
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../db'))

from patient_db import PatientDatabase
patient_db = PatientDatabase()


def to_json(data, http_code):
    headers = {
        'Content-Type': 'application/json'
    }
    return json.dumps(data), http_code, headers


class PatientQueries:
    def __init__(self):
        return

    def query_identifier(self, resource):
        if request.args.get('identifier') == '' or request.args.get('identifier') is None:
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'required',
                         'details': {
                             'text': 'No patient ID provided'
                         }
                     }]}
            return to_json(error, 400)
        else:
            identifier = request.args.get('identifier')
            system, patient_id = identifier.split('|')
            # Retracted below
            if system == '':
                position = '0'
            elif system == '':
                position = '1'
            elif system == '':
                position = '2'
            else:
                error = {'resourceType': 'OperationOutcome',
                         'issue': [{
                             'severity': 'error',
                             'code': 'code-invalid',
                             'details': {
                                 'text': 'Identifying system is not recognized'
                             }
                         }]}
                return to_json(error, 400)
            return patient_db.get_by_identifier(resource, system, patient_id, position)

    def query_gender(self, count):
        if request.args.get('gender') == '' or request.args.get('gender') is None:
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'required',
                         'details': {
                             'text': 'No gender provided'
                         }
                     }]}
            return to_json(error, 400)
        else:
            if request.args.get('gender').lower() != 'm' and request.args.get('gender').lower() != 'f' and request.args.get('gender').lower() != 'u':
                error = {'resourceType': 'OperationOutcome',
                         'issue': [{
                             'severity': 'error',
                             'code': 'code-invalid',
                             'details': {
                                 'text': 'Incorrect gender value'
                             }
                         }]}
                return to_json(error, 400)
            else:
                gender = request.args.get('gender')
                return patient_db.get_by_gender(gender, count)

    def query_logical_id(self):
        logical_id = request.args.get('_id')
        return patient_db.get_by_logical_id(logical_id)

    def query_logical_id_direct(self, logical_id):
        return patient_db.get_by_logical_id(logical_id)

    # Need to adjust for middle_name too
    def query_given_name(self):
        if request.args.get('given'):
            search_type = 1
            given = request.args.get('given')
            return patient_db.get_by_given_name(search_type, given)
        elif request.args.get('given:contains'):
            search_type = 2
            given = request.args.get('given:contains')
            return patient_db.get_by_given_name(search_type, given)
        elif request.args.get('given:exact'):
            search_type = 3
            given = request.args.get('given:exact')
            return patient_db.get_by_given_name(search_type, given)

    def query_family_name(self):
        if request.args.get('family'):
            search_type = 1
            family = request.args.get('family')
            return patient_db.get_by_family_name(search_type, family)
        elif request.args.get('family:contains'):
            search_type = 2
            family = request.args.get('family:contains')
            return patient_db.get_by_family_name(search_type, family)
        elif request.args.get('family:exact'):
            search_type = 3
            family = request.args.get('family:exact')
            return patient_db.get_by_family_name(search_type, family)
