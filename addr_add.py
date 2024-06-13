#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def AddrExists(addr_ip):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT addr_ip FROM Addr WHERE addr_ip = ?''', (addr_ip,))
    addr = cur.fetchone()
    con.close()
    if addr:
        return True
    else:
        return False


def AddrNameExists(addr_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute(
        '''SELECT addr_name FROM Addr WHERE addr_name = ?''', (addr_name,))
    addr = cur.fetchone()
    con.close()
    if addr:
        return True
    else:
        return False


def GetVlanIdByName(vlan_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT vlan_id FROM Vlan WHERE vlan_name = ?''', (vlan_name,))
    vlan_id = cur.fetchone()
    con.close()
    if vlan_id is None:
        return None
    else:
        return vlan_id[0]


def AddAddr(addr_ip, vlan_id, addr_name, addr_desc):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''INSERT INTO Addr(addr_ip, vlan_id, addr_name, addr_desc) VALUES(?, ?, ?, ?)''',
                (addr_ip, vlan_id, addr_name, addr_desc))
    con.commit()
    con.close()


def VlanExists(vlan_id):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT vlan_id FROM Vlan WHERE vlan_id = ?''', (vlan_id,))
    vlan = cur.fetchone()
    con.close()
    if vlan:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(
        description='add an address in the database')
    arggroup = parser.add_mutually_exclusive_group(required=True)
    parser.add_argument('--addrIp', type=LowerCaseString,
                        required=True, help='the address ip')
    arggroup.add_argument('--vlanId', type=int,
                          required=False, help='the vlan id')
    arggroup.add_argument('--vlanName', type=LowerCaseString,
                          required=False, help='the vlan name')
    parser.add_argument('--addrName', type=LowerCaseString,
                        required=True, help='the address name')
    parser.add_argument('--addrDesc', type=LowerCaseString,
                        required=False, default=None, help='the address description')
    args = parser.parse_args()

    if args.vlanName:
        args.vlanId = GetVlanIdByName(args.vlanName)
        if args.vlanId is None:
            print("vlan does not exist")
            sys.exit(1)

    if VlanExists(args.vlanId) is False:
        print("vlan does not exist")
        sys.exit(1)

    if AddrExists(args.addrIp):
        print("address already exists")
        sys.exit(1)

    if AddrNameExists(args.addrName):
        print("address name already exists")
        sys.exit(1)

    AddAddr(args.addrIp, args.vlanId, args.addrName, args.addrDesc)

    sys.exit(0)


if __name__ == '__main__':
    main()
