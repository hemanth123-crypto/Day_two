from model.patient import Patient
from services.healthcare_system import HealthcareSystem
from data.datastore import datastore

system = HealthcareSystem(datastore)

p1=Patient("John Doe", 30, "P001", "Flu")
p2=Patient("Jane Smith", 25, "P002", "Cold")

