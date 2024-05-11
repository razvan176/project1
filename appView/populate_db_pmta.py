import subprocess
from pathlib import Path
import subprocess

def scp_file(host, port, username, remote_path, local_path):
    try:
        scp_command = f"scp -P {port} {username}@{host}:{remote_path} {local_path}"
        subprocess.run(scp_command, shell=True, check=True)
        print(f"File transferred successfully from {remote_path} to {local_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


host = "89.44.100.51"
port = 24
username = "root"
remote_path = "/data/pmta/log/popescu_log/*"
local_path = Path(__file__).resolve().parent.parent/ "appView" / "populate_db" /"logs_pmta"

scp_file(host, port, username, remote_path, local_path)



import os 
from pathlib import Path


def parse_log_line(line):
    parts = line.split()
    id_parts = parts[5].split("|")

    obj = {
        'number_send': parts[0],
        'date': parts[1],
        'hour': parts[2],
        'domain': parts[3],
        'ip': parts[4],
        'id_mint': id_parts[1]
    }
    return obj



def read_log_files():
    log_files = []
    BASE_DIR = Path(__file__).resolve().parent.parent / "appView" / "populate_db" /"logs_pmta"
    processed_files = set()

    # Load processed files
    processed_files_path = BASE_DIR / "processed_files.txt"
    if os.path.exists(processed_files_path):
        with open(processed_files_path, "r") as f:
            processed_files = set(f.read().splitlines())

    for file_name in os.listdir(BASE_DIR):
        if file_name.startswith("log_") and os.path.isfile(os.path.join(BASE_DIR, file_name)):
            if file_name in processed_files:
                print(f"Skipping already processed file: {file_name}")
                continue

            with open(os.path.join(BASE_DIR, file_name), "r") as file:
                log_content = [parse_log_line(line) for line in file]
                log_files.append((file_name, log_content))

            processed_files.add(file_name)

    with open(processed_files_path, "w") as f:
        f.write("\n".join(processed_files))

    return log_files


os.environ.setdefault('DJANGO_SETTINGS_MODULE','appView.settings')
import django
django.setup()
from Raports.models import Set,Pmta,Mint


def populate(obj):
    set_name = Set.objects.get_or_create(set_name=obj['domain'])[0]
    set_name.save()
    pmta =Pmta.objects.get_or_create(set_name=set_name,
                                     date=obj['date'],
                                     hour=obj['hour'],
                                     number_send=obj['number_send'],
                                     ip=obj['ip'],
                                     id_mint=obj['id_mint'])
    mint=Mint.objects.get_or_create(set_name=set_name,
                                     id_mint=obj['id_mint'])


if __name__ == '__main__':
    log_files = read_log_files()
    for file_name, content in log_files:
        for obj in content:
            print(obj)
            populate(obj)