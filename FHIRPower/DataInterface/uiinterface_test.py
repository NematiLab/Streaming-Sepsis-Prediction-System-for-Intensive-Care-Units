from uiinterface import UIInterface

interface = UIInterface('FHIRPower_sepsis_data_interface', 'http://35.188.235.179:8080/baseDstu3')
# Full interface test
interface.initTimedDataLoop('2017-10-02T08:59:59.000-04:00', 5)
#interface.getTimedData('2017-10-02T08:59:59.000-04:00', '2017-10-02T09:05:00.000-04:00')
