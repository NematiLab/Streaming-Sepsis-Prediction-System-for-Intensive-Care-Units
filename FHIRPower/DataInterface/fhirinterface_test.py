from fhirinterface import SmartClient

client = SmartClient('FHIRPower_sepsis_data_interface', 'http://35.188.235.179:8080/baseDstu3')

# Get observations in time range
print "Running getObservationsInTimeRange test"
observation_list = client.getAllPatientObservationsInRange('3', '2017-10-02T08:59:59.000-04:00', '2017-10-02T09:05:00.000-04:00')
for observation in observation_list:
    print observation.code.coding[0].code
    print observation.valueQuantity.value
print "Completed getObservationsInTimeRange test\n"

'''# Add a test patient
print "Running addPatient test"
patient_id = client.addPatientToServer('Dennis', 'Lynch')
print "Created patient id:", patient_id
print "Completed addPatient test\n"'''

'''# Find a patient test
print "Running findPatientById test"
patient = client.getPatientById(patient_id)
print "Patient id of result:", patient.id
print "Completed findPatientById test\n"'''

'''# Find all patients test
print "Running findAllPatients test"
patient_list = client.getAllPatients()
for p in patient_list:
    print "Patient id:", p.id
print "Completed findAllPatients test\n"'''

'''# Add an observation
print "Running addObservation test"
observation_id = client.addObservationToServer('19393', 'bpm', 'bpm', 76.0, '8867-4', 'heartrate', 'http://loinc.org', '2017-10-02T09:00:00.000-04:00')
print "Created observation id:", observation_id
print "Completed addObservation test\n"'''

'''# Find an observation test
print "Running findObservationById test"
observation = client.getObservationById(observation_id)
print "Observation id of result:", observation.id
print "Completed findObservationById test\n"'''

'''# Find all observations for patient
print "Running findObservationsByPatient test"
observation_list = client.getAllPatientObservations('19393')
for obsv in observation_list:
    print "Observation id:", obsv.id
print "Completed findObservationsByPatient test\n"'''

'''# Find all observations for patient and loinc code
print "Running findObservationsByPatientAndLoinc test"
observation_list = client.getPatientObservationByLoinc('19393', '8867-4')
for obsv in observation_list:
    print "Observation id:", obsv.id
print "Completed findObservationsByPatientAndLoinc test\n"'''

'''# Find all observations for patient and timestamp
print "Running findObservationsByPatientAndTimestamp test"
observation_list = client.getPatientObservationsByTimestamp('19393', '2017-10-02T09:00:00.000-04:00')
for obsv in observation_list:
    print "Observation id:", obsv.id
print "Completed findObservationsByPatientAndTimestamp test\n"'''

'''# Find all observations for patient, timestamp, and loinc code
print "Running findObservationsByPatientLoincAndTimestamp test"
observation_list = client.getPatientObservationsByLoincAndTimestamp('19393', '2017-10-02T09:00:00.000-04:00', '8867-4')
for obsv in observation_list:
    print "Observation id:", obsv.id
print "Completed findObservationsByPatientLoincAndTimestamp test\n"'''

'''# Remove test observation
print "Running removeObservation test"
client.removeObservationFromServer(observation_id)
print "Completed removeObservation test\n"'''

'''# Remove test patient
print "Running removePatient test"
client.removePatientFromServer(patient_id)
print "Completed removePatient test"'''