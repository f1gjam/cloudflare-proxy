from __future__ import absolute_import
from __future__ import print_function
import re
import CloudFlare
import yaml
import datetime
import glob, os


def connect():
    cf = CloudFlare.CloudFlare(raw=True)
    return cf


def get_zone_info(cf):
    response = cf.zones.get(params={'per_page': 50})
    total_pages = response['result_info']['total_pages']
    page = 0
    zones = []
    zone_info_dict = {}

    while page <= total_pages:
        page += 1
        response = cf.zones.get(params={'page': page, 'per_page': 50})
        zones.extend(response['result'])

    for zone in zones:
        zone_info_dict[zone['name']] = zone['id']

    return zone_info_dict


def read_yaml_backup_file():
    file_list = []
    zone_record_dict = {}
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

            zone_record_dict[domain[0]] = yaml_load_all(txt_filename)
            print('Finished reading: ' + txt_filename)

    return zone_record_dict


def yaml_load_all(filename):
    with open(filename, 'r') as ymlfile:
        return yaml.load(ymlfile)


def set_proxy(cf, zone_record_dict, set_flag):
    zone_info_dict = get_zone_info(cf)
    count = 0
    for domain_zone in zone_record_dict:
        for single_record in zone_record_dict[domain_zone]:
            count += 1
            for fqdn, record_values in single_record.iteritems():
                print(count)
                if set_flag == True:
                    #Enable proxy ONLY for records which have proxy DISABLED currently - if records have proxy
                    #enabled already skip them (as per backup configuration being read
                    if record_values['proxiable'] == True and record_values['proxied'] == False:
                        print('Enabling Proxy for: ' + fqdn + ' current value: ' +
                              str(record_values['proxied']))
                        enable_proxy(cf, zone_info_dict[domain_zone], fqdn, record_values)
                    else:
                        print('Cannot enable Proxy for: ' + fqdn + ' not proxiable!')
                elif set_flag == False:
                    #Disable proxy ONLY for records who's backup configuration states it should be disabled
                    if record_values['proxiable'] == True and record_values['proxied'] == False:
                        print('Reseting Proxy for: ' + fqdn + 'to original value: ' +
                              str(record_values['proxied']))
                        reset_proxy(cf, zone_info_dict[domain_zone], fqdn, record_values)
                    else:
                        print('Cannot enable Proxy for: ' + fqdn + ' not proxiable!')


def enable_proxy(cf, zone_id, fqdn, record_values):
    dns_record = {
        'zone_id': zone_id,
        'id': record_values['id'],
        'proxied': True,
        'type': record_values['type'],
        'name': fqdn,
        'content': record_values['content'],
        'ttl': record_values['ttl']
    }

    response = cf.zones.dns_records.put(zone_id, record_values['id'], data=dns_record)
    return response


def reset_proxy(cf, zone_id, fqdn, record_values):
    dns_record = {
        'zone_id': zone_id,
        'id': record_values['id'],
        'proxied': record_values['proxied'],
        'type': record_values['type'],
        'name': fqdn,
        'content': record_values['content'],
        'ttl': record_values['ttl']
    }

    response = cf.zones.dns_records.put(zone_id, record_values['id'], data=dns_record)

    return response


def main():
    cf = connect()
    zone_dict = read_yaml_backup_file()
    set_proxy(cf, zone_dict, True)


if __name__ == '__main__':
    main()
