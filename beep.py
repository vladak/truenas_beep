#!/usr/bin/env python3

import argparse
import urllib3
import os

from requests import get


def get_alert_list(uri, headers, verify=True):
    r = get(uri, headers=headers, verify=verify)
    r.raise_for_status()

    return r


def beep():
    dev_speaker="/dev/speaker"
    # copied from spkrtest(8)
    music="msl16oldcd4mll8pcb-agf+4.g4p4<msl16dcd4mll8pa.a+f+4p16g4"

    if os.path.exists(dev_speaker):
       with open(dev_speaker, "w") as f:
           f.write(music)
    else:
       print("speaker device {} does not exist".format(dev_speaker))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Beep on critical TrueNAS alerts')
    parser.add_argument('-T', '--token', help='Bearer token value',
                        required=True)
    parser.add_argument('-U', '--url', help='URL base, e.g. https://foo',
                        required=True)
    parser.add_argument('--noverify', help='do not verify server certificate',
                        action='store_true', default=False)
    parser.add_argument('--dismissed', help='do not avoid dismissed alerts',
                        action='store_true', default=False)
    args = parser.parse_args()

    if args.noverify:
        urllib3.disable_warnings()

    headers = {'accept': '*/*'}
    if args.token:
        headers['Authorization'] = 'Bearer ' + args.token

    l = get_alert_list(args.url + '/api/v2.0/alert/list',
                       headers, verify=not args.noverify)
    for entry in l.json():
        if entry.get('level').lower() == 'critical':
            if entry.get('dismissed') and not args.dismissed:
                continue

            print('{}: {}'.format(entry.get('uuid'), entry.get('formatted')))
            beep()
