# With this script we are going to push the csv file to ipfs and save its cid

from requests import request
import json
import base64
import os 

FILE_PATH = "./Car_Purchasing_Data.csv"
SECRET = os.environ["CHAINSAFE_KEY"]

def create_bucket(bucket_name, secret, encryption_key) :
    url = 'https://api.chainsafe.io/api/v1/buckets'
    payload = json.dumps({
        "type": "fps",
        "name": bucket_name,
        "encryption_key":encryption_key,
        "file_system_type": "chainsafe"
    }) 
    headers = {
        "Authorization": f"Bearer {secret}", 
        "Content-Type": "application/json"
    }

    response = request("POST", url, headers=headers, data=payload)

    return json.loads(response.text)

def upload_files(bucket_id, secret, path_to_file, bucket_subfolder, file_name=None):
    url = f"https://api.chainsafe.io/api/v1/bucket/{bucket_id}/upload"

    payload = {'path': bucket_subfolder}
    if not file_name:
        file_name = path_to_file.split("/")[-1]

    files=[
        ('file',(file_name,open(path_to_file,'rb'),'application/octet-stream'))
    ]
    headers = {
        'Authorization': f'Bearer {secret}'
    }

    # with open(path_to_file, 'rb') as f:
        # requests.post('http://some.url/streamed', data=f)
    response = request("POST", url, headers=headers, data=payload, files=files)
    return json.loads(response.text)

def get_bucket_list(secret):
    url = "https://api.chainsafe.io/api/v1/buckets"

    payload = {}
    headers = {
    'authority': 'api.chainsafe.io',
    'accept': 'application/json',
    'accept-language': 'en-US,en;q=0.9',
    'authorization': f'Bearer {secret}',
    'origin': 'https://app.storage.chainsafe.io',
    'referer': 'https://app.storage.chainsafe.io/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

def download_data(bucket_id, secret, bucket_path_to_file):
    url = f"https://api.chainsafe.io/api/v1/bucket/{bucket_id}/download"

    payload = json.dumps({
    "path": bucket_path_to_file
    })
    headers = {
    'Authorization': f'Bearer {secret}',
    'Content-Type': 'application/json'
    }

    response = request("POST", url, headers=headers, data=payload)
    
    
    return response.content

def write_buffer_to_file(data, path_to_file):
    with open(path_to_file, "wb") as f:
        f.write(data)

def download_data_cid(cid):
    url = f"https://ipfs.chainsafe.io/ipfs/{cid}"
    payload = {}
    headers = {}
    response = request("GET", url, headers=headers, data=payload)

    return response.content




bucket = create_bucket("bucket_car_data", SECRET, "")
bucket_id = bucket["id"]
bucket_subfolder = "/"
uploaded_files=upload_files(bucket_id, SECRET, FILE_PATH, bucket_subfolder)

cids = [u["cid"] for u in uploaded_files["files_details"]]

with open("cids.txt", "w") as f:
    f.write("\n".join(cids))


data_cid = download_data_cid(cids[0])
write_buffer_to_file(data_cid, "./redownloaded_file.csv")

# bucket_path_to_file = bucket_subfolder+FILE_PATH.split("/")[-1]

# data = download_data(bucket_id, SECRET, bucket_path_to_file)

# write_buffer_to_file(data, "/tmp/aaaa_mi_hai_trovato/foto_riscaricata_python.jpg")



