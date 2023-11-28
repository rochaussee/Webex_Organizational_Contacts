import os
import json
from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, flash
import requests

# Create the Flask app and set the secret key to use session variables (for flash messages)
app = Flask(__name__)
app.secret_key = os.getenv('personal_access_token')


# Load the environment variables from the .env file
load_dotenv()

# Get the environment variables
api_url = os.getenv('api_url')
api_url_contacts = os.getenv('api_url_contacts')
refresh_token = os.getenv('refresh_token')
client_id = os.getenv('client_id')
client_secret = os.getenv('client_secret')
org_id = os.getenv('org_id')
personal_access_token = os.getenv('personal_access_token')


# Function to list contacts
def list_contacts():
    access_token = refresh_access_token(f'{api_url}/access_token')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{api_url_contacts}{org_id}/contacts/search', headers=headers)
    return response.json()


# Function to get a contact
def get_contact(contact_id):
    access_token = personal_access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(f'{api_url_contacts}{org_id}/contacts/{contact_id}', headers=headers)
    return response.json()


# Function to create contacts
def create_contacts(firstname, lastname, displayname, companyname=None, email=None, worknumber=None, mobilenumber=None):
    body = {
        "schemas": 'urn:cisco:codev:identity:contact:core:1.0',
        "source": "CH",
        "firstName": firstname,
        "lastName": lastname,
        "displayName": displayname
    }

    if companyname:
        body["companyName"] = companyname
    if email:
        body["emails"] = [{"type": "work", "value": email}]
    phoneNumbers = []
    if worknumber:
        phoneNumbers.append({"type": "work", "value": worknumber})
    if mobilenumber:
        phoneNumbers.append({"type": "mobile", "value": mobilenumber})
    if phoneNumbers:
        body["phoneNumbers"] = phoneNumbers

    access_token = personal_access_token
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    response = requests.post(f'{api_url_contacts}{org_id}/contacts', headers=headers, json=body)
    if response.status_code == 401:
        flash('Personal Access Token expired', 'error')
    else:
        flash('Contact created successfully', 'success')
    return response.json()


# Function to update contacts
def update_contacts(contact_id, firstname=None, lastname=None, displayname=None, companyname=None, email=None, worknumber=None, mobilenumber=None):

    existing_contact = get_contact(contact_id)
    body = {
        "schemas": 'urn:cisco:codev:identity:contact:core:1.0',
        "source": "CH"
    }

    if firstname:
        body["firstName"] = firstname
    if lastname:
        body["lastName"] = lastname
    if displayname:
        body["displayName"] = displayname
    if companyname:
        body["companyName"] = companyname

    phoneNumbers = existing_contact.get('phoneNumbers', [])
    emails = existing_contact.get('emails', [])

    if worknumber:
        for pn in phoneNumbers:
            if pn.get('type') == 'work':
                body.setdefault('phoneNumbers', []).append({"type": "work", "value": pn['value'], "operation": "delete"})
        body.setdefault('phoneNumbers', []).append({"type": "work", "value": worknumber})

    if mobilenumber:
        for pn in phoneNumbers:
            if pn.get('type') == 'mobile':
                body.setdefault('phoneNumbers', []).append({"type": "mobile", "value": pn['value'], "operation": "delete"})
        body.setdefault('phoneNumbers', []).append({"type": "mobile", "value": mobilenumber})

    if email:
        for em in emails:
            if em.get('type') == 'work':
                body.setdefault('emails', []).append({"type": "work", "value": em['value'], "operation": "delete"})
        body.setdefault('emails', []).append({"type": "work", "value": email})


    access_token = personal_access_token
    headers = {'Authorization': f'Bearer {access_token}',
               'Content-Type': 'application/json'}
    response = requests.patch(f'{api_url_contacts}{org_id}/contacts/{contact_id}', headers=headers, json=body)
    if response.status_code == 401:
        flash('Personal Access Token expired', 'error')
    else:
        flash('Contact updated successfully', 'success')
    return response.json()


# Function to delete contacts
def delete_contacts(contact_id):
    access_token = personal_access_token
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.delete(f'{api_url_contacts}{org_id}/contacts/{contact_id}', headers=headers)
    if response.status_code == 401:
        flash('Personal Access Token expired', 'error')
    else:
        flash('Contact deleted successfully', 'success')
    if response.text:  # Check if the response is not empty
        data = response.json()


# Function to get access token using refresh token
def refresh_access_token(url):

    body = {
        'grant_type': 'refresh_token',
        'client_id': client_id,
        'client_secret': client_secret,
        'refresh_token': refresh_token
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=body)
    return json.loads(response.text)['access_token']


# Route to handle home page index.html and all the operations (create, list, update, delete)
@app.route('/', methods=['GET', 'POST'])
def index():
    contacts = None
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'create':
            create_contacts(request.form['firstname'], request.form['lastname'], request.form['displayname'],
                            request.form['companyname'], request.form['email'], request.form['worknumber'],
                            request.form['mobilenumber'])
            return redirect(url_for('index'))

        elif action == 'list':
            contacts = list_contacts()

        elif action == 'delete':
            delete_contacts(request.form['contact_id'])
            return redirect(url_for('index'))

        elif action == 'update':
            update_contacts(request.form['contact_id'], request.form['firstname'], request.form['lastname'],
                            request.form['displayname'], request.form['companyname'], request.form['email'],
                            request.form['worknumber'], request.form['mobilenumber'])
            return redirect(url_for('index'))

    return render_template('index.html', contacts=contacts)


#launch the Flask dev server in debug mode on all interfaces and port 5000:
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('./certs/webexcontacts.pem', './certs/webexcontacts.key'))
