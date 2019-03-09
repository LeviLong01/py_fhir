import json


def to_json(data, http_code):
    headers = {
        'Content-Type': 'application/json'
    }
    return json.dumps(data), http_code, headers


# Follows the STU3 Patient Schema: https://www.hl7.org/fhir/patient.html
class PatientSchema:
    def get_schema(self, data):
        schema = {
            'resourceType': data['resourceType'],
            'id': data['id'],
            'identifier': [
                {
                    'use': data['identifier'][0]['use'],
                    'system': data['identifier'][0]['system'],
                    'value': data['identifier'][0]['value'],
                    "assigner": data['identifier'][0]['assigner']
                },
                {
                    'use': data['identifier'][1]['use'],
                    'system': data['identifier'][1]['system'],
                    'value': data['identifier'][1]['value'],
                    'assigner': data['identifier'][1]['assigner']
                },
                {
                    'use': data['identifier'][2]['use'],
                    'system': data['identifier'][2]['system'],
                    'value': data['identifier'][2]['value'],
                    'assigner': data['identifier'][2]['assigner']
                }
            ],
            'name': [
                {
                    'use': data['name'][0]['use'],
                    'family': data['name'][0]['family'],
                    'given': data['name'][0]['given']
                }
            ],
            'telecom': [
                {
                    'system': data['telecom'][0]['system'],
                    'value': data['telecom'][0]['value'],
                    'use': data['telecom'][0]['use']
                },
                {
                    'system': data['telecom'][1]['system'],
                    'value': data['telecom'][1]['value'],
                    'use': data['telecom'][1]['use']
                },
                {
                    'system': data['telecom'][2]['system'],
                    'value': data['telecom'][2]['value'],
                    'use': data['telecom'][2]['use']
                },
                {
                    'system': data['telecom'][3]['system'],
                    'value': data['telecom'][3]['value'],
                    'use': data['telecom'][3]['use']
                },
                {
                    'system': data['telecom'][4]['system'],
                    'value': data['telecom'][4]['value'],
                    'use': data['telecom'][4]['use']
                }
            ],
            'gender': data['gender'],
            'birthDate': data['birthDate'],
            'address': [
                {
                    'use': data['address'][0]['use'],
                    'line': data['address'][0]['line'],
                    'city': data['address'][0]['city'],
                    'state': data['address'][0]['state'],
                    'postalCode': data['address'][0]['postalCode']
                },
                {
                    'use': data['address'][1]['use'],
                    'line': data['address'][1]['line'],
                    'city': data['address'][1]['city'],
                    'state': data['address'][1]['state'],
                    'postalCode': data['address'][1]['postalCode']
                }
            ]
        }
        return schema
