import sys
sys.path.insert(0, '../../FHIRPower/DataInterface')
from fhirinterface import SmartClient
import csv

csv_relative_file_path = '../demographics.csv'
client = SmartClient('FHIRPower_sepsis_data_interface', 'http://35.188.235.179:8080/baseDstu3')
patient_mapping = {}

# Read in each line and add the patient to the FHIR server
with open(csv_relative_file_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        patient_id = client.addPatientToServer(row['firstname'], row['lastname'])
        patient_mapping[row['patient']] = patient_id

print patient_mapping
print "Finished loading patients into database"




