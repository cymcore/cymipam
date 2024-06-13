#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def GetAddrRecordByIpaddr(addr_ip):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Addr WHERE addr_ip = ?''', (addr_ip,))
    addr = cur.fetchone()
    if addr is None:
        return None
    else:
        columns = [desc[0] for desc in cur.description]
        addrDict = dict(zip(columns, addr))
        con.close()
        return addrDict


def GetAddrRecordByIpName(addr_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Addr WHERE addr_name = ?''', (addr_name,))
    addr = cur.fetchone()
    if addr is None:
        return None
    else:
        columns = [desc[0] for desc in cur.description]
        addrDict = dict(zip(columns, addr))
        con.close()
        return addrDict


def DisplayFormat(addr, displayFormat):
    if displayFormat == 'dict':
        print(addr)

    elif displayFormat == 'block':
        print(f"addr_ip: {addr['addr_ip']}")
        print(f"vlan_id: {addr['vlan_id']}")
        print(f"addr_name: {addr['addr_name']}")
        print(f"addr_desc: {addr['addr_desc']}")
        print()

    elif displayFormat == 'csv':
        headers = addr.keys()
        print(','.join(headers))
        print(
            f"{addr['addr_ip']},{addr['vlan_id']},{addr['addr_name']},{addr['addr_desc']}")

    sys.exit(0)


def main():
    parser = argparse.ArgumentParser(
        description='get an address in the database')
    arggroup = parser.add_mutually_exclusive_group(required=True)
    arggroup.add_argument('--addrIp', type=LowerCaseString,
                        required=False, help='the address ip')
    arggroup.add_argument('--addrName', type=LowerCaseString,
                        required=False, help='the address name')
    parser.add_argument('--displayFormat', type=LowerCaseString,
                        required=False, default='csv', help='the display output format')
    args = parser.parse_args()

    if args.addrIp:
        addr = GetAddrRecordByIpaddr(args.addrIp)
    if args.addrName:
        addr = GetAddrRecordByIpName(args.addrName)
    if addr is None:
        print("address does not exist")
        sys.exit(1)
    else:
        DisplayFormat(addr, args.displayFormat)


if __name__ == '__main__':
    main()
