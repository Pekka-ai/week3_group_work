from collections import defaultdict
from datetime import timedelta, datetime
import psycopg2
from config import config
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import configparser


def upload_to_azure_blob(file_path, container_name, blob_name):

    try:
        config = configparser.ConfigParser()
        config.read('src\\data\\storage_account.ini')
        account_name = config['azure_storage']['account_name']
        account_key = config['azure_storage']['account_key']
        container_name = config['azure_storage']['container_name']
        print(account_name)

        # Yhdistä Azure Blob Storageen
        connection_string = f"DefaultEndpointsProtocol=https;AccountName={account_name};AccountKey={account_key};EndpointSuffix=core.windows.net"
        
        # Luo BlobServiceClient-yhteys
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
        # Luo BlobClient-objekti
        container_client = blob_service_client.get_container_client(container_name)
        
        # Ladataan tiedosto Blobiin
        blob_client = container_client.get_blob_client(blob_name)
        
        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)  # overwrite=True ylikirjoittaa tiedoston jos se on jo olemassa

        print(f"Report uploaded to Azure Blob Storage as {blob_name}")
    
    except Exception as e:
        print(f"Error uploading file to Azure: {e}")


def fetch_consultant_data():
    cursor = None
    con = None
    try:
        # Lue tietokannan asetukset config.py-tiedostosta
        con = psycopg2.connect(**config())
        cursor = con.cursor()
        query = """
        SELECT cs.consultant_id, co.name AS consultant_name, cs.customer_id, cu.name AS customer_name, cs.start_time, cs.end_time, cs.lunch_break
        FROM consultant_sessions cs
        JOIN consultants co ON cs.consultant_id = co.id
        JOIN customers cu ON cs.customer_id = cu.id
        WHERE cs.start_time >= current_date
        """
        cursor.execute(query)

        # Hae kaikki tulokset
        records = cursor.fetchall()

        return records

    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Database connection error: {error}")
        return None

    finally:
        if cursor is not None:
            cursor.close()  
        if con is not None:
            con.close()


def generate_report(records):
    customer_report = defaultdict(lambda: {
        'total_hours': timedelta(),
        'details': [],
        'consultants': defaultdict(lambda: timedelta())  # Konsulttien työajat asiakaskohtaisesti
    })
    
    consultant_total_hours = defaultdict(timedelta)  # Konsultin kokonaistyömäärä kaikkien asiakkaille

    for record in records:
        consultant_id, consultant_name, customer_id, customer_name, start_time, end_time, lunch_break = record
        work_duration = end_time - start_time
        work_duration -= timedelta(minutes=lunch_break)

        customer_report[customer_id]['details'].append({
            'consultant_id': consultant_id,
            'consultant_name': consultant_name,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'start_time': start_time,
            'end_time': end_time,
            'lunch_break': lunch_break,
            'work_duration': work_duration
        })

        customer_report[customer_id]['total_hours'] += work_duration
        customer_report[customer_id]['consultants'][consultant_id] += work_duration
        consultant_total_hours[consultant_id] += work_duration

    # Lisätään aikaleima raportin nimeen
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Muoto: 2025-01-28_14-30-00
    report_filename = f"consultant_report_{timestamp}.txt"

    with open(report_filename, 'w') as f:
        f.write("Consultant Time Report\n")
        f.write("======================\n\n")

        for customer_id, data in customer_report.items():
            customer_name = data['details'][0]['customer_name']  # Oletetaan, että kaikilla asiakas-id:llä on sama nimi
            f.write(f"---- Customer: {customer_name} (ID: {customer_id}) ----\n")
            f.write(f"Total work hours: {data['total_hours']}\n")
            f.write("Detailed records:\n")
            for detail in data['details']:
                # Tiivistetään konsultin työaika yhteen riviin
                f.write(f"  Consultant: {detail['consultant_name']} (ID: {detail['consultant_id']}) | ")
                f.write(f"Start time: {detail['start_time']}, End time: {detail['end_time']} | ")
                f.write(f"Lunch break (min): {detail['lunch_break']} | Work duration: {detail['work_duration']}\n")
            f.write("\n")

            # Lisätään asiakkaan konsulttien yhteiset työajat
            f.write("Consultant total work hours for this customer:\n")
            for consultant_id, work_hours in data['consultants'].items():
                f.write(f"  Consultant ID: {consultant_id} - Total work hours: {work_hours}\n")

            f.write("\n")

        # Lisätään kokonaistyömäärä kaikille asiakkaille
        f.write("======================\n")
        f.write("Consultant total work hours for all customers:\n")
        for consultant_id, total_work_hours in consultant_total_hours.items():
            f.write(f"  Consultant ID: {consultant_id} - Total work hours: {total_work_hours}\n")

    print(f"Report has been created and saved to: {report_filename}")

    # Upload to Azure Blob
    blob_name = f"consultant_report_{timestamp}.txt"  # Blob-nimi sisältää aikaleiman
    upload_to_azure_blob(report_filename, "container_name", blob_name)

    return report_filename


def main():
    # Fetch time tracking data from PostgreSQL
    records = fetch_consultant_data()

    if records:
        # Create report in text format
        report_file = generate_report(records)
        print(f"Report saved to: {report_file}")
    else:
        print("No time tracking data retrieved from the database.")


if __name__ == "__main__":
    main()
