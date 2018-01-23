from fhirinterface import SmartClient
import sqlite3
from SepsisPredictor import models

class SqlInterface:
    def __init__(self):
        pass

    def addPatientToDatabase(self, patient):
        pass

    def addObservationToDatabase(self, patient_id,patient_name,measurement_time,sepsis_score,heart_rate,temperature,o2_saturation,blood_pressure,glasgow_coma_scale,respiratory_rate):
        try:
            if models.Measurement.objects.filter(patient_id=patient_id, measurement_time=measurement_time).exists():
                pass
            else:
                m = models.Measurement()
                m.patient_id=patient_id
                m.patient_name=patient_name
                m.measurement_time=measurement_time
                m.sepsis_score=sepsis_score
                m.heart_rate=heart_rate
                m.temperature=temperature
                m.o2_saturation=o2_saturation
                m.blood_pressure=blood_pressure
                m.glasgow_coma_scale=glasgow_coma_scale
                m.respiratory_rate=respiratory_rate
                m.save()
            return True
        except Exception as e:
            print e
            print 'Record not saved.'
            return False
    
    def retrieveLatestRecord(self, patient_id):
        latest_record = models.Measurement.objects.filter(patient_id=patient_id).order_by('-measurement_time')[:1]
        return latest_record

    def removePatientFromDatabase(self):
        pass

    def removeObservationFromDatabase(self):
        pass

    def findPatientByName(self):
        pass

    def findPatientById(self):
        pass

    def findObservationById(self):
        pass

    def findObservationByPatient(self):
        pass

    def findObservationByPatientAndTime(self):
        pass

    def findObservationByPatientAndLoinc(self):
        pass

    def findObservationByPatientTimeAndLoinc(self):
        pass
