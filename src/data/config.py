from configparser import ConfigParser
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

def get_storage_credentials():
    credential = DefaultAzureCredential()
    keyvault_url = "https://leija-pekka-secrets.vault.azure.net/"
    client = SecretClient(vault_url=keyvault_url, credential=credential)

    host = client.get_secret("database-host").value
    database = client.get_secret("database-name").value
    database_user = client.get_secret("database-user").value
    password = client.get_secret("password").value
    port = client.get_secret("port").value
    
    print("Databasedatabasedatabase")
    print(host +database_user +database_user +database_user +password +port)
    return {
            "host": host,
            "database": database,
            "user": database_user,
            "password": password,
            "port": port
            }



def config(filename='src\\data\\database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db= {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db


