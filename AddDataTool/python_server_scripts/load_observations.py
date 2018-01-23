import sys
sys.path.insert(0, '../../FHIRPower/DataInterface')
from fhirinterface import SmartClient
import csv

client = SmartClient('FHIRPower_sepsis_data_interface', 'http://35.188.235.179:8080/baseDstu3')
patient_mapping = {' 4d46bc59629604b671e43c51385490c0 ': '3', ' 9007636124fa4a42caa84fc025236386 ': '5', ' bac33e5db1d0f9ffe2091044e58a9394 ': '6', ' 89034dfb56c4c5a8c6953beaaec4a26f ': '4'} # Maps patient hex to patient server id
csv_relative_file_path = '../combined.csv'

def main():
    with open(csv_relative_file_path) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            patient_id = patient_mapping[row['patient']]
            timestamp = row['labdate']
            coding_system = 'http://loinc.org'
            # Record heart rate: code=bpm, unit=bpm, coding=8867-4, display=heartrate
            saveObservation(patient_id, 'bpm', 'bpm', row['heartrate'], '8867-4', 'heartrate', coding_system, timestamp)
            # Record sao2: code=percent, unit=percent, coding=59408-5, display=sao2
            saveObservation(patient_id, 'percent', 'percent', row['sao2'], '59408-5', 'sao2', coding_system, timestamp)
            # Record temperature: code=F, unit=F, coding=8310-5, display=temperature
            saveObservation(patient_id, 'F', 'F', row['temperature'], '8310-5', 'temperature', coding_system, timestamp)
            # Record systemicsystolic: code=mmHg, unit=mmHg, coding=35094-2, display=systemicsystolic
            saveObservation(patient_id, 'mmHg', 'mmHg', row['systemicsystolic'], '35094-2', 'systemicsystolic', coding_system, timestamp)
            # Record systemicmean: code=mmHg, unit=mmHg, coding=1111-1, display=systemicmean
            saveObservation(patient_id, 'mmHg', 'mmHg', row['systemicmean'], '1111-1', 'systemicmean', coding_system, timestamp)
            # Record systemicdiastolic: code=mmHg, unit=mmHg, coding=8462-4, display=systemicdiastolic
            saveObservation(patient_id, 'mmHg', 'mmHg', row['systemicdiastolic'], '8462-4', 'systemicdiastolic', coding_system, timestamp)
            # Record respiration: code=bpm, unit=bpm, coding=9304-7, display=respiration
            saveObservation(patient_id, 'bpm', 'bpm', row['respiration'], '9304-7', 'respiration', coding_system, timestamp)
            # Record etco2: code=percent, unit=percent, coding=33437-5, display=etco2
            saveObservation(patient_id, 'percent', 'percent', row['etco2'], '33437-5', 'etco2', coding_system, timestamp)

    print "Completed loading in observations"

def saveObservation(patient_id, value_code, value_unit, value_quantity, coding_code, coding_display, coding_system, timestamp):
    if value_quantity != 'NULL':
        client.addObservationToServer(patient_id, value_code, value_unit, float(value_quantity), coding_code, coding_display, coding_system, str(timestamp))

'''# Add an observation to database
    # patient_id: The id of the patient subject
    # value_code: The code of the observation value
    # value_unit: The unit of the observation value
    # value_quantity: The quantity of the observation value
    # coding_code: The code of the observation coding
    # coding_display: The display value of the observation coding
    # coding_system: The system associated with the code type
    # timestamp: The time of the observation
    # return: The id of the created observation
    def addObservationToServer(self, patient_id, value_code, value_unit, value_quantity, coding_code, coding_display, coding_system, timestamp):'''

if __name__ == '__main__':
    main()
        

