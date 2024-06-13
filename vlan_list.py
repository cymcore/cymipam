#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def ListVlan():
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Vlan''')
    vlans = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    vlanList = []
    for row in vlans:
        vlanDict = dict(zip(columns, row))
        vlanList.append(vlanDict)
    con.close()

    return vlanList


def DisplayFormat(vlans, displayFormat):
    if displayFormat == 'dict':
        print(vlans)

    elif displayFormat == 'block':
        for vlan in vlans:
            print(f"vlan_id: {vlan['vlan_id']}")
            print(f"vlan_name: {vlan['vlan_name']}")
            print(f"vlan_network: {vlan['vlan_network']}")
            print(f"vlan_cidr: {vlan['vlan_cidr']}")
            print(f"vlan_gateway: {vlan['vlan_gateway']}")
            print(f"vlan_desc: {vlan['vlan_desc']}")
            print()

    elif displayFormat == 'csv':
        headers = vlans[0].keys()
        print(','.join(headers))
        for vlan in vlans:
            print(
                f"{vlan['vlan_id']},{vlan['vlan_name']},{vlan['vlan_network']},{vlan['vlan_cidr']},{vlan['vlan_gateway']},{vlan['vlan_desc']}")

    


def main():
    parser = argparse.ArgumentParser(
        description='remove a vlan in the database')
    parser.add_argument('--displayFormat', type=LowerCaseString,
                        required=False, default='csv', help='the display output format')
    args = parser.parse_args()

    vlans = ListVlan()

    if not vlans:
        print("no vlans exist")
        sys.exit(1)
    else:
        DisplayFormat(vlans, args.displayFormat)
        
    sys.exit(0)

if __name__ == '__main__':
    main()
