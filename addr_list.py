#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def ListAddr():
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Addr''')
    addrs = cur.fetchall()

    columns = [desc[0] for desc in cur.description]
    addrList = []
    for row in addrs:
        addrDict = dict(zip(columns, row))
        addrList.append(addrDict)
    con.close()

    return addrList


def DisplayFormat(addrs, displayFormat):
    if displayFormat == 'dict':
        print(addrs)

    elif displayFormat == 'block':
        for addr in addrs:
            print(f"addr_ip: {addr['addr_ip']}")
            print(f"vlan_id: {addr['vlan_id']}")
            print(f"addr_name: {addr['addr_name']}")
            print(f"addr_desc: {addr['addr_desc']}")
            print()
    elif displayFormat == 'csv':
        headers = addrs[0].keys()
        print(','.join(headers))
        for addr in addrs:
            print(
                f"{addr['addr_ip']},{addr['vlan_id']},{addr['addr_name']},{addr['addr_desc']}")

    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description='list addresses in the database')
    parser.add_argument('--displayFormat', type=LowerCaseString,
                        required=False, default='csv', help='the display output format')
    args = parser.parse_args()


    addrs = ListAddr()

    if not addrs:
        print('no addresses exist')
        sys.exit(0)
    else:
        DisplayFormat(addrs, args.displayFormat)


if __name__ == '__main__':
    main()
