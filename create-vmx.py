import yaml
import argparse
import re
from pathlib import Path


def substitute(specs, template, nodeRole):
    for key, value in specs.items():
        search = f"{{{key}}}"

        if isinstance(value, dict):
            if key == 'role':
                template = substitute(value.get(nodeRole), template, nodeRole)
            else:
                template = substitute(value, template, nodeRole)
        else:
            template = re.sub(search, value, template)

    return template


parser = argparse.ArgumentParser(description="Parses cluster.yaml and generates \".vmx\" files for VMWare which then can be used to register vms.",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("input", type=argparse.FileType(
    'r'), help="Location of the \"cluster.yaml\"")


args = parser.parse_args()
with args.input as file:
    cluster = yaml.safe_load(file)

specs_file = Path("resources/vm-specs.yaml")
with specs_file.open() as file:
    specs = yaml.safe_load(file)

template_file = Path("resources/template.vmx")
with template_file.open() as f:
    template = f.read()

nodes = cluster['cluster']['nodes']

for node in nodes:
    out_dir_name = Path(node['hostname'])
    if not Path.exists(out_dir_name):
        Path.mkdir(out_dir_name)
    else:
        raise Exception("Output folder exists!")

    specs.update([("hostname", node['hostname'])])

    vmxFileName = f"{out_dir_name}/{specs['hostname']}.vmx"
    with open(vmxFileName, mode="w", encoding="UTF-8") as vmx:
        vmx.write(substitute(specs, template, node['role']))

