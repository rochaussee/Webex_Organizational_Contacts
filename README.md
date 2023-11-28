# Webex_Organizational_Contacts
This is a custom Webex App web application that leverage Webex's public APIs for managing Organizational Contacts.

With the help of this custom app, users who are not "Webex Control Hub Admins" can directly manage the Webex Contacts database through their own Webex App. This eliminates the need for interacting with a Webex Admin for this routine task.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Installation

Follow these steps to set up your development environment and install the project's dependencies.

1. **Clone the Repository:**

   Clone this GitHub repository to your local machine using the following command:

   ```bash
   git clone https://github.com/rochaussee/Webex_Organizational_Contacts.git

2. **Navigate to the Project Directory and unzip the .zip files:**
   
   Change your current directory to the project's directory:
   
   ```bash
   cd Webex_Organizational_Contacts
   unzip certs.zip
   unzip templates.zip

    ```
3. **Install Dependencies:**

    Use pip to install the project's dependencies from the requirements.txt file:
   
    ```bash
    pip install -r requirements.txt
    ```
    This will install all the required packages and libraries.

## Usage
   
This project requires a Webex authorization token that includes the 'Identity:contact' scope. You can acquire such an authorization token by setting up a Service App.

For more information on this process, please refer to: https://developer.webex.com/docs/service-apps.
  
Upon creating a Service App, you'll receive the necessary elements (refresh token, client_id, client_secret) to generate a new Access Token.
 
The "personal access token" (Full Admin personal token) is only required because, as of now, Service Apps do not support Create/Update/Delete operations (this feature is currently in the backlog).

Also, given that the Webex App's "Embedded App" framework only supports applications over HTTPS, you will need to create & import your own private key and certificate for this custom app. OpenSSL can be utilized to generate a private key and a Certificate Signing Request (CSR).

1. **Replace the .env file according your environment:**

   Copy the necessary authentication elements (as explained above) with the corresponding ones from your environment.

2. **Replace the private key and certificate by the ones you have generated/signed:**

   Copy the "your_cert_key.key" and "your_signed_cert.pem" files in the "certs" folder with the corresponding files from your environment.
   Also, modify the code according the name of your imported files at the end of the code :
   ```bash
   ssl_context=('./certs/your_cert.pem', './certs/your_key.key'))

4. **Create a Webex Embedded App:**

   Create a "Sidebar" Embedded App on the Webex Developer portal. This will be configured with the URL of your custom app (for example: https://webexcontacts.domain.com:5000). The code utilizes Flask as its web application framework, operating on the default port 5000.

   For more information on this process, please refer to: https://developer.webex.com/docs/embedded-apps

5. **Execute the script:**
   
   Having configured the project with your own .env file, private key, and certificate, you can now proceed to execute it as follows:
   ```bash
   python Webex_contacts_web.py
   ```
6. **Validate your custom app is visible and working through the Webex App:**

   ![image](https://github.com/rochaussee/Webex_Organizational_Contacts/assets/109152368/ac0c0b78-9e65-474e-9cd3-d5ec8c0d83e9)

7. **Validate the List/Created/Updated/Deleted operations:**

   Ensure that the operations performed through this custom app are accurately reflected in the Control Hub Contacts database (navigate to Users -> Contacts to check).


**Note:** We recommend testing the script first on a Webex sandbox environment before using it in a production environment. You can create a sandbox account by following the instructions in the [Webex Developer Sandbox Guide](https://developer.webex.com/docs/developer-sandbox-guide).

## Contributing

We welcome contributions from the community to improve and enhance this project. Whether you want to fix a bug, add a new feature, or simply improve the documentation, your help is greatly appreciated.

## License

This project is open-source and available under the [MIT License](LICENSE.md).
