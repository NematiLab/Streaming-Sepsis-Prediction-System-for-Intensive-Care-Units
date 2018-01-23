from sqlinterface import SqlInterface

a = SqlInterface()
a.addObservationToDatabase(123,'Joel','2017-01-01T01:01:01',0.0,0.0,0.0,0.0,0.0,0.0,0.0)

print a.retrieveLatestRecord('3')
