# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Measurement
from bokeh.plotting import figure
from bokeh.embed import components
from DataInterface import uiinterface
import time

origin_timestamp = '2017-10-02T08:59:59.000-04:00'
origin_timestamp_str = origin_timestamp[:len(origin_timestamp) - 6]
origin_time = datetime.strptime(origin_timestamp_str, '%Y-%m-%dT%H:%M:%S.%f')

def index(request):
    start_time = origin_time
    range_delta = timedelta(minutes=5)
    end_time = start_time + range_delta
    update_time = end_time + timedelta(hours=4)

    starting_timestamp = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
    ending_timestamp = datetime.strftime(end_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'

    ui = uiinterface.UIInterface('FHIRPower_sepsis_data_interface', 'http://35.199.27.148:8080/baseDstu3')
    ui.getTimedData(starting_timestamp, ending_timestamp)
    # time.sleep(5)

    # context = get_sepsis_score_context(update_time)
    # print context
    context = {}
    return render(request, 'SepsisPredictor/index.html', context)

def get_data(request, increment):
    delta = timedelta(minutes=int(increment))
    start_time = origin_time + delta
    range_delta = timedelta(minutes=5)
    end_time = start_time + range_delta
    update_time = end_time + timedelta(hours=4) #this is done to account for the time-zone difference

    starting_timestamp = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
    ending_timestamp = datetime.strftime(end_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'

    ui = uiinterface.UIInterface('FHIRPower_sepsis_data_interface', 'http://35.199.27.148:8080/baseDstu3')
    ui.getTimedData(starting_timestamp, ending_timestamp)

    patient_list = Measurement.objects.filter(measurement_time=update_time).order_by('-sepsis_score')

    patient_id_list = patient_list.values_list('patient_id').distinct()

    patient_ids = []
    for x in patient_id_list:
        patient_ids.append(x[0])

    bundle = []

    for i in patient_ids:
        data = []
        patient_data = Measurement.objects.filter(patient_id=i).order_by('measurement_time')[:20]
        score_data = []
        time_data = []
        for p in patient_data:
            score_data.append(getattr(p, 'sepsis_score'))
            time_data.append(getattr(p, 'measurement_time'))
        plot = figure(x_axis_label='Time',
                      y_axis_label='Score',
                      x_axis_type='datetime',
                      y_range=(0, 1),
                      plot_width=800,
                      plot_height=200)
        plot.circle(time_data[-1], score_data[-1], size=10, color='red')
        plot.line(time_data, score_data, line_width=2, color='red')
        script, div = components(plot)
        data.append(patient_data.last())
        data.append(script)
        data.append(div)
        bundle.append(data)

    context = {'bundle': bundle} #bundle = {id: data}, data[0] = patient, data[1] = script, data[2] = div
    return render(request, 'SepsisPredictor/get_data.html', context)

def get_detail_data(request, patient_id, increment):
    delta = timedelta(minutes=int(increment))
    start_time = origin_time + delta
    range_delta = timedelta(minutes=5)
    end_time = start_time + range_delta

    starting_timestamp = datetime.strftime(start_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'
    ending_timestamp = datetime.strftime(end_time, '%Y-%m-%dT%H:%M:%S') + '.000-04:00'

    ui = uiinterface.UIInterface('FHIRPower_sepsis_data_interface', 'http://35.199.27.148:8080/baseDstu3')
    ui.getTimedData(starting_timestamp, ending_timestamp)

    patient_history = Measurement.objects.filter(patient_id=patient_id).order_by('measurement_time')[:20]

    patient = patient_history.last()

    time_data = []
    hr_data = []
    temp_data = []
    o2_data = []
    bp_data = []
    gcs_data = []
    rr_data = []

    # Heart Rate
    for hr_measure in patient_history:
        hr_data.append(getattr(hr_measure, 'heart_rate'))
        time_data.append(getattr(hr_measure, 'measurement_time'))
    hr_plot = figure(x_axis_label='Time',
                     y_axis_label='Rate',
                     x_axis_type='datetime',
                     plot_width=800,
                     plot_height=200)
    hr_plot.circle(time_data[-1], hr_data[-1], size=10, color='red')
    hr_plot.line(time_data, hr_data, line_width=2, color='red')
    hr_context = components(hr_plot)

    # Temperature
    for temp_measure in patient_history:
        temp_data.append(getattr(temp_measure, 'temperature'))
    temp_plot = figure(x_axis_label='Time',
                     y_axis_label='Rate',
                     x_axis_type='datetime',
                     plot_width=800,
                     plot_height=200)
    temp_plot.circle(time_data[-1], temp_data[-1], size=10, color='red')
    temp_plot.line(time_data, temp_data, line_width=2, color='red')
    temp_context = components(temp_plot)

    # O2 Saturation
    for o2_measure in patient_history:
        o2_data.append(getattr(o2_measure, 'o2_saturation'))
    o2_plot = figure(x_axis_label='Time',
                     x_axis_type='datetime',
                     y_axis_label='Saturation',
                     plot_width=800,
                     plot_height=200)
    o2_plot.circle(time_data[-1], o2_data[-1], size=10, color='red')
    o2_plot.line(time_data, o2_data, line_width=2, color='red')
    o2_context = components(o2_plot)

    # Blood Pressure
    for bp_measure in patient_history:
        bp_data.append(getattr(bp_measure, 'blood_pressure'))
    bp_plot = figure(x_axis_label='Time',
                     x_axis_type='datetime',
                     y_axis_label='Pressure',
                     plot_width=800,
                     plot_height=200)
    bp_plot.circle(time_data[-1], bp_data[-1], size=10, color='red')
    bp_plot.line(time_data, bp_data, line_width=2, color='red')
    bp_context = components(bp_plot)

    # Glasgow Coma Scale
    for gcs_measure in patient_history:
        gcs_data.append(getattr(gcs_measure, 'glasgow_coma_scale'))
    gcs_plot = figure(x_axis_label='Time',
                      y_axis_label='Scale',
                      x_axis_type='datetime',
                      plot_width=800,
                      plot_height=200)
    gcs_plot.circle(time_data[-1], gcs_data[-1], size=10, color='red')
    gcs_plot.line(time_data, gcs_data, line_width=2, color='red')
    gcs_context = components(gcs_plot)

    # Respiratory Rate
    for rr_measure in patient_history:
        rr_data.append(getattr(rr_measure, 'respiratory_rate'))
    rr_plot = figure(x_axis_label='Time',
                     y_axis_label='Rate',
                     x_axis_type='datetime',
                     plot_width=800,
                     plot_height=200)
    rr_plot.circle(time_data[-1], rr_data[-1], size=10, color='red')
    rr_plot.line(time_data, rr_data, line_width=2, color='red')
    rr_context = components(rr_plot)

    context = {'patient': patient, 'hr': hr_context, 'temp': temp_context, 'o2': o2_context, 'bp': bp_context, 'gcs': gcs_context, 'rr': rr_context}
    return render(request, 'SepsisPredictor/get_detail_data.html', context)

def detail(request, patient_id):
    most_recent_measure = Measurement.objects.filter(patient_id=patient_id).order_by('-measurement_time').first()
    update_time = getattr(most_recent_measure, 'measurement_time')
    print update_time
    patient = Measurement.objects.get(patient_id=patient_id, measurement_time=update_time)

    time_passed = update_time.replace(tzinfo=None) - origin_time - timedelta(hours=4)
    current_increment = int(divmod(time_passed.total_seconds(), 60)[0])

    context = {'patient': patient, 'update_time': update_time, 'current_increment': current_increment}
    return render(request, 'SepsisPredictor/detail.html', context)
