import sys
from ruamel.yaml import YAML

LOCAL_PATH = './'
yaml = YAML()
data = yaml.load(sys.stdin.read())
top_volumes = data.get('volumes', {})
services = data.get('services', {})
converted_volumes = set()

if not services:
    sys.exit()


def convert(volumes):
    result = []
    for volume in volumes:
        if (isinstance(volume, str) and
                not volume.startswith(LOCAL_PATH)):
            converted_volumes.add(volume[:volume.find(':')])
            volume = LOCAL_PATH + volume
        elif (isinstance(volume, dict) and
                volume.get('source') and
                not volume['source'].startswith(LOCAL_PATH)):
            volume['source'] = LOCAL_PATH + volume['source']
        result.append(volume)

    return result


for key in services.keys():
    service_volumes = convert(services[key].get('volumes', []))
    if service_volumes:
        services[key]['volumes'] = service_volumes

for volume in converted_volumes:
    if volume in top_volumes.keys():
        top_volumes.pop(volume)

if not top_volumes:
    data.pop('volumes')

yaml.dump(data, sys.stdout)
