from fhirclient import client
import fhirclient.models.patient as p
import fhirclient.models.observation as o
import fhirclient.models.bundle as b
import fhirclient.models.humanname as hn
import fhirclient.models.coding as c
import fhirclient.models.codeableconcept as cc
import fhirclient.models.fhirdate as d
import fhirclient.models.quantity as q
import fhirclient.models.fhirreference as r
import requests


class SmartClient:
    def __init__(self, app_id, api_base):
        self.settings = {
            'app_id': app_id,
            'api_base': api_base
        }

        self.smart = client.FHIRClient(settings=self.settings)

    # Get one patient by id
    # patient_id: The FHIR Server id of the patient resource
    # return: The patient object associated with the id
    def getPatientById(self, patient_id):
        return p.Patient.read(str(patient_id), self.smart.server)

    # Get all patients in database
    # return: A list of patient objects for all patients
    def getAllPatients(self):
        return self.getPagedResults(b.Bundle.read_from(self.settings['api_base'] + '/Patient', self.smart.server))

    # Get one observation by id
    # observation_id: The id of the requested observation
    # return: The requested observation object
    def getObservationById(self, observation_id):
        return o.Observation.read(str(observation_id), self.smart.server)

    # Get all observations by patient
    # patient_id: The id of the patient whose observations you want
    # return: List of observation objects associated with the patient
    def getAllPatientObservations(self, patient_id):
        search = o.Observation.where(struct={'subject': str(patient_id)})
        return self.getPagedResults(search.perform(self.smart.server))

    def getAllPatientObservationsInRange(self, patient_id, start_time, end_time):
        search = o.Observation.where(struct={'subject': str(patient_id), 'date': '>={}'.format(str(start_time)),
                                             'date': '<{}'.format(str(end_time))})
        return self.getPagedResults(search.perform(self.smart.server))

    # Get all observations by patient and LOINC
    # patient_id: The id of the patient whose observations you want
    # loinc_code: The loinc code associated with the observations you want
    # return: List of observation objects associated with the patient and loinc code
    def getPatientObservationByLoinc(self, patient_id, loinc_code):
        search = o.Observation.where(struct={'subject': str(patient_id), 'code': str(loinc_code)})
        observations = self.getPagedResults(search.perform(self.smart.server))
        return observations

    # Get all observations by patient and timestamp
    # patient_id: The id of the patient whose observations you want
    # timestamp: The timestamp associated with the observations you want
    # return: List of observation objects associated with the patient and timestamp
    def getPatientObservationsByTimestamp(self, patient_id, timestamp):
        search = o.Observation.where(struct={'subject': str(patient_id), 'date': str(timestamp)})
        observations = self.getPagedResults(search.perform(self.smart.server))
        return observations

    # Get all observations by patient, timestamp, and LOINC
    # patient_id: The id of the patient whose observations you want
    # timestamp: The timestamp associated with the observations you want
    # loinc_code: The loinc code associated with the observations you want
    def getPatientObservationsByLoincAndTimestamp(self, patient_id, timestamp, loinc_code):
        search = o.Observation.where(
            struct={'subject': str(patient_id), 'code': str(loinc_code), 'date': str(timestamp)})
        observations = self.getPagedResults(search.perform(self.smart.server))
        return observations

    # Add a patient to database
    # given_name: The first name of the patient
    # family_name: The last name of the patient
    # return: The id of the created patient (None if not created)
    def addPatientToServer(self, given_name, family_name):
        patient = p.Patient()
        name = hn.HumanName()
        name.given = [given_name]
        name.family = [family_name]
        patient.name = [name]
        result_json = patient.create(self.smart.server)
        patient.id = self.getCreatedId(result_json)
        return patient.id

    # Add an observation to database
    # patient_id: The id of the patient subject
    # value_code: The code of the observation value
    # value_unit: The unit of the observation value
    # value_quantity: The quantity of the observation value
    # coding_code: The code of the observation coding
    # coding_display: The display value of the observation coding
    # coding_system: The system associated with the code type
    # timestamp: The time of the observation
    # return: The id of the created observation
    def addObservationToServer(self, patient_id, value_code, value_unit, value_quantity, coding_code, coding_display,
                               coding_system, timestamp):
        observation = o.Observation()
        # Create Value Quantity
        quantity = q.Quantity()
        quantity.code = value_code
        quantity.unit = value_unit
        quantity.value = value_quantity
        observation.valueQuantity = quantity

        # Create Coding
        code = cc.CodeableConcept()
        coding_item = c.Coding()
        coding_item.code = coding_code
        coding_item.display = coding_display
        coding_item.system = coding_system
        coding_list = [coding_item]
        code.coding = coding_list
        observation.code = code

        # Create Subject
        reference = r.FHIRReference()
        reference.reference = self.getPatientById(patient_id).relativePath()
        observation.subject = reference

        # Create Status
        observation.status = 'final'

        # Create Issued/EffectiveDateTime
        observation.effectiveDateTime = d.FHIRDate(timestamp)

        # Write the observation
        result_json = observation.create(self.smart.server)
        observation.id = self.getCreatedId(result_json)
        return observation.id

    # Remove a patient from database
    # patient_id: The id in the FHIR database of the patient to remove
    def removePatientFromServer(self, patient_id):
        patient = self.getPatientById(patient_id)
        patient.delete()

    # Remove an observation from database
    # observation_id: The id in the FHIR database of the observation to remove
    def removeObservationFromServer(self, observation_id):
        observation = self.getObservationById(observation_id)
        observation.delete()

    # Extract the created id from a creation result json blob
    # input_json: The json response from the FHIR server after successful resource creation
    # return: The id of the created resource
    def getCreatedId(self, input_json):
        created_id = None
        if input_json != None:
            diagnostic_string = input_json['issue'][0]['diagnostics']
            created_id = (diagnostic_string.split(' ')[3]).split('/')[1]

        return created_id

    # Page through a bundle to get all available resources
    # initial_bundle: The bundle request that will initiate the search
    # return: A list of all of the requested resources
    def getPagedResults(self, initial_bundle):
        output_list = []
        paging = True
        bundle = initial_bundle
        while paging:
            bundle_list = bundle.entry
            for bundle_item in bundle_list:
                output_list.append(bundle_item.resource)
                print bundle_item.resource
            bundle_link_list = bundle.link
            paging = False
            for bundle_link in bundle_link_list:
                if bundle_link.relation == 'next':
                    paging = True
                    bundle = b.Bundle.read_from(bundle_link.url, self.smart.server)
        return output_list
