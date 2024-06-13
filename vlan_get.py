#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def GetVlanRecordByVlanId(vlan_id):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Vlan WHERE vlan_id = ?''', (vlan_id,))
    vlan = cur.fetchone()
    if vlan is None:
        return None
    else:
        columns = [desc[0] for desc in cur.description]
        vlanDict = dict(zip(columns, vlan))
        con.close()
        return vlanDict


def GetVlanRecordByVlanName(vlan_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Vlan WHERE vlan_name = ?''', (vlan_name,))
    vlan = cur.fetchone()
    if vlan is None:
        return None
    else:
        columns = [desc[0] for desc in cur.description]
        vlanDict = dict(zip(columns, vlan))
        con.close()
        return vlanDict


def DisplayFormat(vlan, displayFormat):
    if displayFormat == 'dict':
        print(vlan)

    elif displayFormat == 'block':
        print(f"vlan_id: {vlan['vlan_id']}")
        print(f"vlan_name: {vlan['vlan_name']}")
        print(f"vlan_network: {vlan['vlan_network']}")
        print(f"vlan_cidr: {vlan['vlan_cidr']}")
        print(f"vlan_gateway: {vlan['vlan_gateway']}")
        print(f"vlan_desc: {vlan['vlan_desc']}")
        print()

    elif displayFormat == 'csv':
        headers = vlan.keys()
        print(','.join(headers))
        print(f"{vlan['vlan_id']},{vlan['vlan_name']},{vlan['vlan_network']},{vlan['vlan_cidr']},{vlan['vlan_gateway']},{vlan['vlan_desc']}")


def main():
    parser = argparse.ArgumentParser(description='get a vlan in the database')
    arggroup = parser.add_mutually_exclusive_group(required=True)
    arggroup.add_argument('--vlanId', type=int,
                          required=False, help='the vlan id')
    arggroup.add_argument('--vlanName', type=LowerCaseString,
                          required=False, help='the vlan name')
    parser.add_argument('--displayFormat', type=LowerCaseString,
                        required=False, default='csv', help='the display output format')
    args = parser.parse_args()

    if args.vlanId is not None:
        vlan = GetVlanRecordByVlanId(args.vlanId)
    elif args.vlanName is not None:
        vlan = GetVlanRecordByVlanName(args.vlanName)

    if vlan is None:
        print('vlan does not exist')
        sys.exit(1)
    else:
        DisplayFormat(vlan, args.displayFormat)

    sys.exit(0)


if __name__ == '__main__':
    main()
