import numpy as np
from numpy import pi
import subprocess
import time

from bokeh.client import push_session
from bokeh.driving import cosine
from bokeh.plotting import figure, curdoc
from bokeh.io import output_file, show
from bokeh.layouts import row, column
from random import *
from bokeh.models import Range1d
import datetime

##KICK OFF BOKEH SERVER

# com = subprocess.Popen.send_signal()
command1 = subprocess.Popen(['bokeh', 'serve'])
# command2 = subprocess.Popen(['python', 'printtt.py'])

output_file("layout.html")


##INIT DATA
patient1SepsisData = []
patient2SepsisData = []
patient3SepsisData = []
patient4SepsisData = []

patient1SepsisData.append(.9)
patient2SepsisData.append(.9)
patient3SepsisData.append(.9)
patient4SepsisData.append(.9)

##SET UP THE STARTING DATE FOR THE PLOT
##THIS WILL NEED TO BE CHANGED TO THE FIRST ELEMENT FO THE DATA
Xaxis = []
myDate = datetime.datetime(100,1,1,11,34,59)
Xaxis.append(myDate)

plotWidth = 800
plotHeight = 200

##SET UP PLOTS
##THIS IS WHERE THE PATIENT NAME IS SET
patient1FIGURE = figure(x_axis_label='Time',
                  y_axis_label='Score',
                  plot_width=plotWidth,
                  plot_height=plotHeight,
                  y_range=(0, 1.4),
                  x_axis_type="datetime",
                  title="Patient 1")
patient1FIGURE.title.text_color = "green"
patient1FIGURE.title.text_font_size = '25pt'
r1 = patient1FIGURE.line(Xaxis, [1]*len(Xaxis), color="firebrick")
r2 = patient1FIGURE.line(Xaxis,patient1SepsisData, color="navy", line_width=4)

patient2FIGURE = figure(x_axis_label='Time',
                  y_axis_label='Score',
                  plot_width=plotWidth,
                  plot_height=plotHeight,
                  y_range=(0, 1.4),
                  x_axis_type="datetime",
                  title="Patient 2")
patient2FIGURE.title.text_color = "green"
patient2FIGURE.title.text_font_size = '25pt'
r3 = patient2FIGURE.line(Xaxis, [1]*len(Xaxis), color="firebrick")
r4 = patient2FIGURE.line(Xaxis,patient2SepsisData, color="navy", line_width=4)

patient3FIGURE = figure(x_axis_label='Time',
                  y_axis_label='Score',
                  plot_width=plotWidth,
                  plot_height=plotHeight,
                  y_range=(0, 1.4),
                  x_axis_type="datetime",
                  title="Patient 3")
patient3FIGURE.title.text_color = "green"
patient3FIGURE.title.text_font_size = '25pt'
r5 = patient3FIGURE.line(Xaxis, [1]*len(Xaxis), color="firebrick")
r6 = patient3FIGURE.line(Xaxis,patient3SepsisData, color="navy", line_width=4)

patient4FIGURE = figure(x_axis_label='Time',
                  y_axis_label='Score',
                  plot_width=plotWidth,
                  plot_height=plotHeight,
                  y_range=(0, 1.4),
                  x_axis_type="datetime",
                  title="Patient 4")
patient4FIGURE.title.text_color = "green"
patient4FIGURE.title.text_font_size = '25pt'
r7 = patient4FIGURE.line(Xaxis, [1]*len(Xaxis), color="firebrick")
r8 = patient4FIGURE.line(Xaxis,patient4SepsisData, color="navy", line_width=4)

# open a session to keep our local document in sync with server
session = push_session(curdoc())

##THIS OPENS A TAB IN YOUR BROWSER FOR VIEWING THE PLOT - THE ORDER OF THE PLOTS CAN BE SET HERE
session.show(column(patient1FIGURE, patient2FIGURE, patient3FIGURE, patient4FIGURE))

for i in range(100):

    ##HERE IS WHERE WE POPULATE THE LOCAL ARRAY OF SEPSIS DATA
    ##THIS IS WHERE THE SEPSIS PREDICTOR WILL NEED TO BE CALLED
    ##CURRENTLY I AM ADDING RANDOM DATA
    patient1SepsisData.append(1.25 - random())
    patient2SepsisData.append(1.25 - random())
    patient3SepsisData.append(1.25 - random())
    patient4SepsisData.append(1.25 - random())

    ##HERE I ITERATE THE TIME BY 300 SECONDS (5 MINUTES)
    myDate = myDate + datetime.timedelta(0, 300)
    Xaxis.append(myDate)

    ##HERE I TRIM THE DATA TO THE LATEST 20 DATAPOINTS TO KEEP THE CONTEXT OF THE DATA CONSISTENT
    if len(patient1SepsisData)==20:
        patient1SepsisData.pop(0)
        patient2SepsisData.pop(0)
        patient3SepsisData.pop(0)
        patient4SepsisData.pop(0)
        Xaxis.pop(0)

    ##UPDATE THE FIGURES WITH THE LATEST DATA
    r1.data_source.data["y"] = [1] * len(Xaxis)
    r1.data_source.data["x"] = Xaxis
    r2.data_source.data["y"] = patient1SepsisData
    r2.data_source.data["x"] = Xaxis

    r3.data_source.data["y"] = [1] * len(Xaxis)
    r3.data_source.data["x"] = Xaxis
    r4.data_source.data["y"] = patient2SepsisData
    r4.data_source.data["x"] = Xaxis

    r5.data_source.data["y"] = [1] * len(Xaxis)
    r5.data_source.data["x"] = Xaxis
    r6.data_source.data["y"] = patient3SepsisData
    r6.data_source.data["x"] = Xaxis

    r7.data_source.data["y"] = [1] * len(Xaxis)
    r7.data_source.data["x"] = Xaxis
    r8.data_source.data["y"] = patient4SepsisData
    r8.data_source.data["x"] = Xaxis

    patient1FIGURE.update()
    patient2FIGURE.update()
    patient3FIGURE.update()
    patient4FIGURE.update()

    ##THIS IS WHERE I SET THE TIME DELAY
    time.sleep(.5)