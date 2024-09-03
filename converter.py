import sys
from ruamel.yaml import YAML


SERVICE_PREFIX = 'sentry-'
LOCAL_PATH = './'


def convert(volumes):
    result = []
    for volume in volumes:
        if str(volume).startswith(SERVICE_PREFIX):
            volume = LOCAL_PATH + volume
        result.append(volume)
    return result


yaml = YAML()
data = yaml.load(sys.stdin.read())
volumes = data.get('volumes', {})
services = [service[len(SERVICE_PREFIX):] for service in volumes.keys() if
            service.startswith(SERVICE_PREFIX)]

if services:
    serv = data.get('services', {})
    for key in serv.keys():
        if key in services:
            converted_volumes = convert(serv[key]['volumes'])
            serv[key]['volumes'] = converted_volumes
            volumes.pop(SERVICE_PREFIX + key)
    data['volumes'] = volumes
    yaml.dump(data, sys.stdout)
else:
    sys.stdout.write('Script didn`t find services with named volumes\n')
