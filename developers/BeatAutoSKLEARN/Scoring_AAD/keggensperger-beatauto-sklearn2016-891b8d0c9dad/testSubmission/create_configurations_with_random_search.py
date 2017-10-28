import argparse
import json
import tempfile
import os
import zipfile

from ConfigSpace.io import pcs

parser = argparse.ArgumentParser()
parser.add_argument('configuration_space', type=str)
parser.add_argument('output_directory', type=str)
parser.add_argument('-n', default=10, type=int)

args = parser.parse_args()

config_space_path = args.configuration_space
output_directory = args.output_directory
n = args.n

with open(config_space_path) as fh:
    config_space_string = fh.read().split('\n')

config_space = pcs.read(config_space_string)

try:
    os.makedirs(output_directory)
except:
    pass

if not os.path.exists(output_directory):
    print('Could not create output directory.')
    exit(1)

configurations = config_space.sample_configuration(n)

for i, configuration in enumerate(configurations):
    values = configuration.get_dictionary()
    new_values = {}
    for key, value in values.items():
        if value is not None:
            new_values[key] = value
    config_json = json.dumps(new_values, indent=4, sort_keys=True)
    json_file_name = 'hp.json'
    with open(json_file_name, 'w') as fh:
        fh.write(config_json)

    output_name = os.path.join(output_directory, 'hp_%d.json.zip' % i)
    zf = zipfile.ZipFile(output_name, mode='w')
    zf.write(json_file_name)
    zf.close()

    os.remove(json_file_name)