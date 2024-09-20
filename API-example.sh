#!/bin/bash

# modify the endpoint to the correct address
ENDPOINT=localhost:8000

# Obtain token
# parameters: 'username', 'password'
# response: 'token'
curl -X POST -H "Content-Type: application/json" \
             -d '{
    "username": "jinjei",
    "password": "jinjei"
}' $ENDPOINT/api-token-auth/

# copy the token from the response
TOKEN='c6047687d93259ae9b97484d44542fd5ecc54521'

# Create clinic
# send https request to create clinic
# parameters: 'name', 'phone', 'address', 'email', 'city', 'state'
curl -X POST -H "Content-Type: application/json" \
             -H "Authorization: Token $TOKEN" \
             -d '{
    "name": "Clinic x",
    "phone": "1234567890",
    "address": "1234 Main St",
    "email": "1@gamil.com",
    "city": "San Francisco",
    "state": "CA"
}' $ENDPOINT/api/clinics/

# Create doctor
# parameters: 'npi', 'name', 'email', 'phone', 'specialties'
curl -X POST -H "Content-Type: application/json" \
             -H "Authorization: Token $TOKEN" \
             -d '{
    "npi": "1234567890",
    "name": "Doctor x",
    "email": "1@gmail.com",
    "phone": "1234567890",
    "specialties": ["CR", "CL"]
}' $ENDPOINT/api/doctors/

# Create patient
# parameters: 'name', 'phone', 'address', 'birth_date', 'ssn', 'gender'
curl -X POST -H "Content-Type: application/json" \
             -H "Authorization: Token $TOKEN" \
             -d '{
    "name": "Patient x",
    "phone": "1234567890",
    "address": "1234 Main St",
    "birth_date": "1990-01-01",
    "ssn": "123456789",
    "gender": "M"
}' $ENDPOINT/api/patients/

# Get Clinic info
# parameters: 'id': clinic id
# exmple response 1:
#    {"id": 3, "name": "Clinic 1", "phone": "1234567890", "email": "a@gamil.com", "city": "San Francisco", "state": "CA", "address": "1234 Main St"}
# example response 2:
#    {"error": "clinic not found"}
curl -X GET -H "Authorization: Token $TOKEN" $ENDPOINT/api/clinics/1/
