import psycopg2
import psycopg2.extras
import json


def to_json(data, http_code):
    headers = {
        'Content-Type': 'application/json'
    }
    return json.dumps(data), http_code, headers


class PatientDatabase:
    def __init__(self):
        self.conn_string = "host='' dbname='' user='' password=''"
        self.conn = psycopg2.connect(self.conn_string)
        return

    def get_args(self):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT message_body FROM fhir.patient")

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)

    def get_by_identifier(self, system, patient_id, position):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'identifier' -> " + position + " ->> 'system' = '" + system + "' " +
                           "AND message_body -> 'identifier' -> " + position + " ->> 'value' = '" + patient_id + "'")

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)

    def get_by_gender(self, gender, count):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            if count == -1:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body ->> 'gender' = '" + gender + "'")
            else:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body ->> 'gender' = '" + gender + "' LIMIT " + count)

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)

    def get_by_logical_id(self, logical_id):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body ->> 'id' = '" + logical_id + "'")

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)

    # Need to adjust for middle_name too
    def get_by_given_name(self, search_type, given):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            if search_type == 1:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 -> 'given' ->> 0 LIKE '" + given + "%'")
            elif search_type == 2:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 -> 'given' ->> 0 LIKE '%" + given + "%'")
            elif search_type == 3:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 -> 'given' ->> 0 = '" + given + "'")

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)

    def get_by_family_name(self, search_type, family):
        try:
            patients = []
            cursor = self.conn.cursor('cursor_unique_name', cursor_factory=psycopg2.extras.DictCursor)
            if search_type == 1:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 ->> 'family' LIKE '" + family + "%'")
            elif search_type == 2:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 ->> 'family' LIKE '%" + family + "%'")
            elif search_type == 3:
                cursor.execute("SELECT message_body FROM fhir.patient WHERE message_body -> 'name' -> 0 ->> 'family'  =  '" + family + "'")

            for row in cursor:
                patients.append((row['message_body']))

            self.conn.close()
            return to_json(patients, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)
    """
    def insert_new_patient(self, json_data):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO fhir.patient (wellness_id, resource_type, first_name, last_name, message_body) "
                           "VALUES ('" + json_data['identifier'][0]['value'] + "','patient','" +
                           json_data['name'][0]['given'][0] + "','" + json_data['name'][0]['family'] + "','" + json.dumps(json_data) + "')")
            self.conn.commit()
            self.conn.close()
            return to_json(json_data, 200)

        except Exception as e:
            # Return thrown error
            error = {'resourceType': 'OperationOutcome',
                     'issue': [{
                         'severity': 'error',
                         'code': 'invalid',
                         'details': {
                             'text': e
                         }
                     }]}
            return to_json(error, 400)
    """
