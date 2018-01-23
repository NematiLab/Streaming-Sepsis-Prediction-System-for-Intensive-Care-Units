# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

# Create your models here.

class Measurement(models.Model):
    patient_id = models.IntegerField(default=0)
    patient_name = models.CharField(max_length=200)
    measurement_time = models.DateTimeField(default=timezone.now)
    sepsis_score = models.FloatField(default=0)
    heart_rate = models.FloatField(default=0, null=True)
    temperature = models.FloatField(default=0, null=True)
    o2_saturation = models.FloatField(default=0, null=True)
    blood_pressure = models.FloatField(default=0, null=True)
    glasgow_coma_scale = models.FloatField(default=0, null=True)
    respiratory_rate = models.FloatField(default=0, null=True)

    def __str__(self):
        outStr = '\r\nPatient ID: %s\r\n' % self.patient_id
        outStr += 'Patient Name: %s\r\n' % self.patient_name
        outStr += 'Measurement Time: %s\r\n' % self.measurement_time
        outStr += 'Sepsis Score: %s\r\n' % self.sepsis_score
        return outStr

    def delete_everything(self):
        Measurement.objects.all().delete()
