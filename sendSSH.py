import requests
import json

a = {
    "key":"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCj8c3/peGePmcYIoNoEbtuzoxTZCZ/LqgIS8V6lZVYe8QpuqElETMBKE5irOxm0OwvrP0FA3iOmI64cZHeMrvO7c6j371aYt8HyCYCXsY0ptaEUZC8rv2fPZjJSYb1kAjB8mfkVg6JI2GEgiIZP0zJI/53H2L7euVXFmFR+3AEDT8RuK2fttpHOce7bNUmLMvK/W24KoPMRFmKI5+AdD0r/6CswUp2MNt9ff/801v9LyZjLsbHC+vSA3Z9A75tg8yIrkDBl8DA9HfclQJFG0PTMkVSVD7+GtUuE0ncHs4nsrO9Gj1qLfyoh584JHGKsx3AgB18tX7Kiw+kJ+QBYHzP 1727405109"
}

url = "https://pandora.sumsc.xin/ssh"

res = requests.post(url,json=a) #json=json.dumps(a))

print(res.status_code)

print(res.text)