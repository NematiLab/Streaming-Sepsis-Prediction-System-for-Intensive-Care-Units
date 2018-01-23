from fhirinterface import SmartClient
from sqlinterface import SqlInterface
from datetime import datetime, timedelta
#import get_sepsis_score_python
from fake_sepsis_scorer import FakeSepsisScorer
from SepsisPredictor import models
import time

class UIInterface:
    def __init__(self, app_id, api_base):
        self.smartclient = SmartClient(app_id, api_base)
        self.sqlinterface = SqlInterface()
        s = FakeSepsisScorer()
        #s = get_sepsis_score_python.initialize()
        self.sepsis_scorer = s

    def initTimedDataLoop(self, starting_timestamp, max_iterations=None):
        # Starting timestamp of format '2017-10-02T08:59:59.000-04:00'
        # Initialize starting values
        starting_timestamp_str = starting_timestamp[:len(starting_timestamp) - 6]
        starting_date = datetime.strptime(starting_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
        delta = timedelta(minutes=5)
        ending_date = starting_date + delta
        starting_timestamp_current = datetime.strftime(starting_date, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
        ending_timestamp_current = datetime.strftime(ending_date, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
        
        current_iterations = 0
        done = False
        # Loop until we've hit max iterations, or keep looping until done
        while ((max_iterations!= None and current_iterations < max_iterations) or (max_iterations == None and done == False)):
            print('Starting Time: {}'.format(starting_timestamp_current))
            print('Ending Time: {}'.format(ending_timestamp_current))
            done = not self.getTimedData(starting_timestamp_current, ending_timestamp_current)
            ending_timestamp_str = ending_timestamp_current[:len(ending_timestamp_current) - 6]
            ending_timestamp_new = datetime.strptime(ending_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
            ending_date_new = ending_timestamp_new + delta
            starting_timestamp_current = ending_timestamp_current
            ending_timestamp_current = datetime.strftime(ending_date_new, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
            current_iterations += 1
            time.sleep(5)
        

    def getTimedData(self, starting_timestamp, ending_timestamp):
        # Get all patient observations within timeframe
        data_added = False
        patient_list = self.smartclient.getAllPatients()
        for patient in patient_list:
            observation_map = {
                '8867-4': None,  # Heart Rate
                '59408-5': None,  # sao2
                '8310-5': None,  # Temperature
                '35094-2': None,  # systemicsystolic
                '1111-1': None,  # systemicmean
                '8462-4': None,  # systemicdiastolic
                '9304-7': None,  # respiration
                '33437-5': None  # etco2
            }
            # Get observations in time range
            observations = self.smartclient.getAllPatientObservationsInRange(patient.id, starting_timestamp,
                                                                             ending_timestamp)
            for observation in observations:
                observation_map[observation.code.coding[0].code] = observation.valueQuantity.value

            # Get most recent observation from database
            latest_observation = self.sqlinterface.retrieveLatestRecord(str(patient.id)).first()
            if latest_observation is not None:
                # (l_pid, l_name, l_time, l_score, l_hr, l_temp, l_sao2, l_bp, l_etco2, l_resp) = latest_observation.all()[0]
                l_pid = getattr(latest_observation, 'patient_id')
                l_name = getattr(latest_observation, 'patient_name')
                l_time = getattr(latest_observation, 'measurement_time')
                l_score = getattr(latest_observation, 'sepsis_score')
                l_hr = getattr(latest_observation, 'heart_rate')
                l_temp = getattr(latest_observation, 'temperature')
                l_sao2 = getattr(latest_observation, 'o2_saturation')
                l_bp = getattr(latest_observation, 'blood_pressure')
                l_etco2 = getattr(latest_observation, 'glasgow_coma_scale')
                l_resp = getattr(latest_observation, 'respiratory_rate')
                if observation_map['8867-4'] == None:
                    observation_map['8867-4'] = l_hr
                if observation_map['59408-5'] == None:
                    observation_map['59408-5'] = l_sao2
                if observation_map['8310-5'] == None:
                    observation_map['8310-5'] = l_temp
                if observation_map['1111-1'] == None:
                    observation_map['1111-1'] = l_bp
                if observation_map['9304-7'] == None:
                    observation_map['9304-7'] = l_resp
                if observation_map['33437-5'] == None:
                    observation_map['33437-5'] = l_etco2

            if len(observations) > 0:
                data_added = True

            patient_name = '{} {}'.format(patient.name[0].given[0], patient.name[0].family[0])
            print patient_name, observation_map
            # Perform the sepsis score calculation
            null = 0.0
            if latest_observation is not None:
                sepsis_score = self.sepsis_scorer.get_sepsis_score_python(getattr(latest_observation, 'sepsis_score'))
            else:
                sepsis_score = self.sepsis_scorer.get_sepsis_score_python()
            # sepsis_score = self.sepsis_scorer.get_sepsis_score_python(
            #     observation_map['8867-4'] if observation_map['8867-4'] != None else null,
            #     observation_map['59408-5'] if observation_map['59408-5'] != None else null,
            #     observation_map['8310-5'] if observation_map['8310-5'] != None else null,
            #     observation_map['35094-2'] if observation_map['35094-2'] != None else null,
            #     observation_map['1111-1'] if observation_map['1111-1'] != None else null,
            #     observation_map['8462-4'] if observation_map['8462-4'] != None else null,
            #     observation_map['9304-7'] if observation_map['9304-7'] != None else null,
            #     observation_map['33437-5'] if observation_map['33437-5'] != None else null,
            #     null, null, null, null, null, null, null, null, null,
            #     null, null, null, null, null, null, null, null, null,
            #     null, null, null, null, null, null, null, null, null)
            print sepsis_score

            # Store the data in the SQL-Lite database
            # TODO: Map coma score to a reading
            # TODO: Determine which blood pressure reading to incorporate into database
            self.sqlinterface.addObservationToDatabase(patient.id, patient_name, ending_timestamp, sepsis_score,
                                                       observation_map['8867-4'], observation_map['8310-5'],
                                                       observation_map['59408-5'], observation_map['1111-1'],
                                                       observation_map['33437-5'], observation_map['9304-7'])
        return data_added
