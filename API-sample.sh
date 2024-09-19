#!/bin/bash

# modify the endpoint to the correct address
ENDPOINT=localhost:8000

# Create clinic
# send https request to create clinic
# parameters: 'name', 'phone', 'address', 'email', 'city', 'state'
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Clinic 1",
    "phone": "1234567890",
    "address": "1234 Main St",
    "email": "1@gamil.com",
    "city": "San Francisco",
    "state": "CA"
}' $ENDPOINT/clinics/

# Create doctor
# parameters: 'npi', 'name', 'email', 'phone', 'specialties'
curl -X POST -H "Content-Type: application/json" -d '{
    "npi": "1234567890",
    "name": "Doctor 1",
    "email": "1@gmail.com",
    "phone": "1234567890",
    "specialties": ["CR", "CL"]
}' $ENDPOINT/doctors/

# Create patient
# parameters: 'name', 'phone', 'address', 'birth_date', 'ssn', 'gender'
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Patient 1",
    "phone": "1234567890",
    "address": "1234 Main St",
    "birth_date": "1990-01-01",
    "ssn": "123456789",
    "gender": "M"
}' $ENDPOINT/patients/