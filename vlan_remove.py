#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def VlanExistsByVlanId(vlan_id):
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


def RemoveVlanByVlanId(vlan_id):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''DELETE FROM Vlan WHERE vlan_id = ?''', (vlan_id,))
    con.commit()
    con.close()


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


def main():
    parser = argparse.ArgumentParser(
        description='remove a vlan in the database')
    arggroup = parser.add_mutually_exclusive_group(required=True)
    arggroup.add_argument('--vlanId', type=int,
                          required=False, help='the vlan id')
    arggroup.add_argument('--vlanName', type=LowerCaseString,
                          required=False, help='the vlan id')
    args = parser.parse_args()

    if args.vlanName:
        args.vlanId = GetVlanIdByName(args.vlanName)
        if args.vlanId is None:
            print("vlan does not exist")
            sys.exit(1)

    if VlanExistsByVlanId(args.vlanId) is False:
        print("vlan does not exist")
        sys.exit(1)

    RemoveVlanByVlanId(args.vlanId)
    sys.exit(0)


if __name__ == '__main__':
    main()
