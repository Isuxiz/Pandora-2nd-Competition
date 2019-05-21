import requests
import json

a = {
    "key":"86:f5:7e:95:8f:f0:17:a5:14:26:48:4d:b0:e0:8c:2e",
    "commit":"1727405109"
}

url = "https://pandora.sumsc.xin/ssh"

res = requests.post(url,json=a)#json=json.dumps(a))

print(res.status_code)

print(res.text)