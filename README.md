# Dental Management Platform

## Setup
**Note** This project is developed in python 3.10.4

### Create virtual environment
```
python -m venv env
```
### Set up virtual environment
- **For MAC/Linux**
```
source env/bin/activate
```
- **For Windows**
```
.\env\Scripts\activate
```
### Install dependencies
**Note**: You may need to install postgresql on your local machine to install certain modules.
```
pip install -r requirements.txt
```
### PostgreSQL Configuation
Fill up `dental_platform/dental_platform/.env` to allow your server connect to the database. You can check out `dental_platform/dental_platform/.env.template` to see which field you have to fill.

This step requires you to prepare a PostreSQL. An easy way to create a databse is to use docker.
Here is the [guidance](./postgres.md)

### Setup Django Project
```
cd dental_platform
```
```
python manage.py makemigrations
```
```
python manage.py migrate
```
#### Set up a user to access the system
```
python manage.py createsuperuser --username=joe --email=joe@example.com
```
### Run Server
```
python manage.py runserver
```
## How to use
- The home page is in `localhost:8000/`
- Login using the superuser you created earlier
- The public API calls are in the `API-example.sh`. You can check the input parameters

## Rest APIs
| API path | Method | Introduction | payload | output |
| -------- | ------ | ------------ | ----- | ------ |
| / | GET | homepage | | html page |
| /clinics | GET | clinic page  | | html page |
| /doctors | GET | doctor page  | | html page |
| /patients | GET | patient page  | | html page |
| /clinics/:clinic_id | GET | clinic detail page  | | html page |
| /doctors/:doctors_id | GET | doctor detail page  | | html page |
| /patients/:patient_id | GET | patient detail page  | | html page |
| /clinics/:clinic_id/edit/ | POST | update clinic command  | ['id', 'name', 'phone', 'address', 'email', 'city', 'state'] | redirect |
| /doctors/:doctors_id/edit/ | POST | update doctor command  | ['id', 'npi', 'name', 'email', 'phone', 'specialties'] | redirect |
| /patients/:patient_id/edit/ | POST | update patient command  | ['id', 'name', 'phone', 'address', 'birth_date', 'ssn', 'gender'] | redirect |
| /api/clinics/ | POST | add new clinic, public API interface  | see `API-example.sh` | { sucess: true/false} |
| /api/doctors/ | POST | add new doctor, public API interface  | see `API-example.sh` | { sucess: true/false} |
| /api/patients/ | POST | add new patient, public API interface  | see `API-example.sh` | { sucess: true/false} |
| /api/clinics/:clinic_id/ | GET | get clinic information without affiliated patients and doctors | see `API-example.sh` | see `API-example.sh` |
| /clinics/int:clinic_id/affliations/ | POST | add clinic doctor affliation along with their working schedule | Form data | redirect/Error |
| /patients/int:patient_id/add_appointment/ | GET | get the page for making appointment | | html page |
| /ajax/clinics/' | GET | loading correspoding component given previous selection | | html component |
| /ajax/doctors/' | GET | loading correspoding component given previous selection | | html component |
| /ajax/patients/int:patient_id/appointments | POST | make appointment | AppointmentForm | redirect |

## Assumptions
1. One patient can have multiple appointments, but we only shows the most recent one.
1. You cannot add any affliation when you create clinics, doctors, patients
1. Affliations associated with patients can only be added when adding an appointment/visit
1. Affliations between clinic and doctor are unique among database.
1. Use code for predefined specialties (CL: cleaning, CR: Crown, FL: Filling, RC: Root Canal, WH: Whitening)