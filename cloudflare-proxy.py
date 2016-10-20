import re

import CloudFlare
import yaml
import datetime
import glob, os




def connect():
    cf = CloudFlare.CloudFlare(raw=True)
    return cf



def read_yaml_backup_file():
    file_list = []
    zone_dict = {}
    os.chdir("/tmp")
    for file in glob.glob("cloudflare-backup-dns-*.yml"):
        file_list.append(file)

    for file in file_list:
        txt_filename = file

        re1 = '.*?'  # Non-greedy match on filler
        re2 = '((?:[a-z][a-z\\.\\d_]+)\\.(?:[a-z\\d]{3}))(?![\\w\\.])'  # File Name 1

        rg = re.compile(re1 + re2, re.IGNORECASE | re.DOTALL)
        m = rg.search(txt_filename)
        if m:
            file1 = m.group(1)
            domain = file1.split('.yml')

            zone_dict[domain[0]] = yaml_load_all(txt_filename)
            print('Finished reading: ' + txt_filename)

    return zone_dict


def yaml_load_all(filename):
    with open(filename, 'r') as ymlfile:
        return yaml.load(ymlfile)


def enable_proxy(zone_dict):
    for all_records in zone_dict:
        for single_record in zone_dict[all_records]:
            print(single_record)
            for key, value in single_record.iteritems():
                if value['proxiable'] == True:
                    print('Enabling Proxy for: ' + key)
                else:
                    print('Cannot enable Proxy for: ' + key)

def main():
    cf = connect()
    zone_dict = read_yaml_backup_file()
    enable_proxy(zone_dict)



if __name__ == '__main__':
    main()
