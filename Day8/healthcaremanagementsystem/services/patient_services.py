class PatientServices:
    def __init__(self, datastore):
        self.datastore = datastore

    def add_patient(self, patient):
        if patient in self.datastore["patient"]:
            self.datastore["patient"][patient._id] = patient

    def get_patient(self, patient_id):
        return self.datastore["patient"].get(patient_id).display_info()

    def update_patient(self, patient_id, updated_data):
        if patient_id in self.datastore["patient"]:
            self.datastore["patient"][patient_id].ailment=ailment

    def delete_patient(self, patient_id):
        if patient_id in self.datastore["patient"]:
            del self.datastore["patient"][patient_id]