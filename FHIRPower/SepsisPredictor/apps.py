# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
# from datetime import datetime, timedelta

class SepsisPredictorConfig(AppConfig):
    name = 'SepsisPredictor'
    def ready(self):
        # from DataInterface import uiinterface
        from SepsisPredictor import models

        m = models.Measurement()
        m.delete_everything()

        # origin_timestamp = '2017-10-02T08:59:59.000-04:00'
        # origin_timestamp_str = origin_timestamp[:len(origin_timestamp) - 6]
        #
        #
        # start_time = datetime.strptime(origin_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')
        # range_delta = timedelta(minutes=5)
        # end_time = start_time + range_delta
        #
        # starting_timestamp = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
        # ending_timestamp = datetime.strftime(end_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
        #
        # ui = uiinterface.UIInterface('FHIRPower_sepsis_data_interface', 'http://35.188.235.179:8080/baseDstu3')
        # ui.getTimedData(starting_timestamp, ending_timestamp)