# Webex_Organizational_Contacts
Custom web application leveraging the Webex public APIs for Organizational Contacts

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

2. **Navigate to the Project Directory:**
   
   Change your current directory to the project's directory:
   
   ```bash
   cd Webex_Organizational_Contacts

    ```
3. **Install Dependencies:**

    Use pip to install the project's dependencies from the requirements.txt file:
   
    ```bash
    pip install -r requirements.txt
    ```
    This will install all the required packages and libraries.

## Usage
   
The project requires a Webex auth token with a scope of Identity:contact.
You can obtain an auth token with a scope of Identity:contact by creating a Service App :
https://developer.webex.com/docs/service-apps
  
With a Service App, you will obtain the required elements to generate a new Access Token :
    - refresh token
    - client_id
    - client_secret
    - org_id
 
 The "personal access token" (Full Admin personal token) is only need because Creating/Updating/Deleting operations are not supported by Service App as of today (in backlog).

1. **Replace the .env file according your environment:**

 Replace the required authentication elements (explained above) by the ones of your environment.

2. **Execute the script:**
   
Now that you've configured the project with your API auth tokens, you can execute it as follows:
   ```bash
   python Webex_contacts_web.py
   ```

**Note:** We recommend testing the script first on a Webex sandbox environment before using it in a production environment. You can create a sandbox account by following the instructions in the [Webex Developer Sandbox Guide](https://developer.webex.com/docs/developer-sandbox-guide).

## Contributing

We welcome contributions from the community to improve and enhance this project. Whether you want to fix a bug, add a new feature, or simply improve the documentation, your help is greatly appreciated.

## License

This project is open-source and available under the [MIT License](LICENSE.md).
