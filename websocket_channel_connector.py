import requests
import json

url = "https://CLUSTER_ID.piesocket.com/api/publish"
payload = json.dumps({
    "key": "oCdCMcMPQpbvNjUIzqtvF1d2X2okWpDQj4AwARJuAgtjhzKxVEjQU6IdCjwm", #Demo key, get yours at https://piesocket.com
    "secret": "d8129f82f8dd71910aa4a7efa30a7297", #Demo secret, get yours at https://piesocket.com
    "roomId": 1,
    "message": { "text": "Hello world!" }
});
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data = payload)
print(response.text.encode('utf8'))