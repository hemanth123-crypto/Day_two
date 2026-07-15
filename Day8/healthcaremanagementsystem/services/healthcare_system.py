from services.patient_service import PatientServices

class HealthcareSystem:
    def __init__(self, datastore):
        self.datastore = datastore
        self.patient_services = PatientServices(datastore)

    