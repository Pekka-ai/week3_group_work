# week3_group_work 🚀
# Consultant Sessions API
This is a Flask-based REST API for managing consultant sessions, consultants, and customers. The application connects to a PostgreSQL database and provides endpoints to create, retrieve, update, and delete consultant sessions. It also includes functionality for generating reports and uploading them to Azure Blob Storage.

## Features
- Manage Consultant Sessions (CRUD operations).
- Handle Consultants and Customers.
- Store and retrieve data using PostgreSQL.
- Generate customer and consultant reports based on session data.
- Upload reports to Azure Blob Storage.
  
## Setup & Installation: 

1. Clone the repository:
    - git clone https://github.com/Pekka-ai/week3_group_work.git
3. Install dependencies:
    - pip install -r requirements.txt
3. Set up the database:Configure PostgreSQL credentials in config.py.
4. Run the application:python app.py

## API Endpoints

Consultants:

`GET /consultants → Get all consultants.`  
`POST /consultants → Create a consultant.`

Customers:

`GET /customers → Get customers.`
`POST /customers → Create a customer.`

Consultant Sessions:

`GET /consultant_sessions → Get all sessions.`
`POST /consultant_sessions → Create a session.`
`PUT /consultant_sessions/<id> → Update a session.`
`DELETE /consultant_sessions/<id> → Delete a session`

Reports:
`POST /reports → Create reports in Azure and the root folder.`
  

## Running the Project on a Virtual Machine (Linux-based)
Connect to the virtual machine via the Azure Portal.

Update the package list:
- sudo apt update
  
Install necessary dependencies:
- sudo apt install python3 python3-pip python3-venv
  
Clone the project repository:
- git clone https://github.com/Pekka-ai/week3_group_work.git

If you encounter permission issues:
  - If you run into problems related to file or directory permissions, you may need to set up a group on the virtual machine and assign the necessary permissions.
  - Please refer to the section "Creating a group on the virtual machine and assigning the necessary permissions" for further instructions on how to resolve permission issues.

Navigate to the project folder:
- cd week3_group_work

Set up a Python virtual environment:
- python3 -m venv venv

Activate the virtual environment:
- . venv/bin/activate

## Creating a group on the virtual machine and assigning the necessary permissions:

Create a new group, for example, projectgroup, if it doesn't already exist:
- sudo groupadd projectgroup

Assign the group to the desired directory:
- sudo chown -R :projectgroup /home/project

Now, the directory belongs to the projectgroup group, but users cannot modify it yet.
Set read, write, and execute permissions for the group:
- sudo chmod -R 2775 /home/project

Explanation:
2 = New files will automatically inherit this group.
775 = The owner and group can read, write, and execute within the directory, while others can only read.

Add users to the projectgroup group:
- sudo usermod -aG projectgroup azureuser
- sudo usermod -aG projectgroup aku.ankka@ankkalinna.ai

Ask users to log out and back in for the group settings to take effect.

Verify that everything is working:
- ls -ld /home/project

TThe result should look like this:
- drwxrwxr-x 3 root projectgroup 4096 Jan 29 07:45 /home/project
  - d: Indicates that it is a directory.
  - rwx: The owner (root) has read (r), write (w), and execute (x) permissions for files in this directory.
  - rwx: The group (projectgroup) has the same permissions as the owner: read, write, and execute.
  - r-x: Others have permission to read and execute files, but not write.

he command getent group shows all the users belonging to a specific group:
- getent group projectgroup
