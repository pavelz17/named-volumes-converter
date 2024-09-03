import sys
from ruamel.yaml import YAML


LOCAL_PATH = './'
yaml = YAML()
data = yaml.load(sys.stdin.read())
top_volumes = data.get('volumes', {})
services = data.get('services', {})
converted_volumes = set()


def convert(volumes):
    result = []
    for mount in volumes:
        if (isinstance(mount, str) and
                not mount.startswith(LOCAL_PATH)):
            converted_volumes.add(mount[:mount.find(':')])
            mount = LOCAL_PATH + mount
        elif isinstance(mount, dict):
            src = mount.get('source')
            if src and not src.startswith(LOCAL_PATH):
                mount['source'] = LOCAL_PATH + src
        result.append(mount)

    return result


if services:
    for key in services.keys():
        service_volumes = services[key].get('volumes', [])
        if service_volumes:
            service_volumes = convert(service_volumes)
            services[key]['volumes'] = service_volumes

    for volume in converted_volumes:
        if volume in top_volumes.keys():
            top_volumes.pop(volume)

    if top_volumes:
        data['volumes'] = top_volumes
    else:
        data.pop('volumes')
        
    yaml.dump(data, sys.stdout)
else:
    sys.stdout.write('Script didn`t find services\n')
