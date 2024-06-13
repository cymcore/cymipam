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


def VlanExistsByVlanNameAndVlanId(vlan_name, vlan_id):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute(
        '''SELECT vlan_name FROM Vlan WHERE vlan_name = ? AND vlan_id = ?''', (vlan_name, vlan_id))
    vlan = cur.fetchone()
    con.close()
    if vlan:
        return True
    else:
        return False


def UpdateVlan(vlan_id, vlan_name, vlan_network, vlan_cidr, vlan_gateway, vlan_desc):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''UPDATE Vlan SET vlan_name = ?, vlan_network = ?, vlan_cidr = ?, vlan_gateway = ?, vlan_desc = ? WHERE vlan_id = ?''',
                (vlan_name, vlan_network, vlan_cidr, vlan_gateway, vlan_desc, vlan_id))
    con.commit()
    con.close()


def VlanExistsByVlanName(vlan_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute(
        '''SELECT vlan_name FROM Vlan WHERE vlan_name = ?''', (vlan_name,))
    vlan = cur.fetchone()
    con.close()
    if vlan:
        return True
    else:
        return False


def main():
    parser = argparse.ArgumentParser(description='add a vlan in the database')
    parser.add_argument('--vlanId', type=int,
                        required=True, help='the vlan id')
    parser.add_argument('--vlanName', type=LowerCaseString,
                        required=True, help='the vlan name')
    parser.add_argument('--vlanNetwork', type=LowerCaseString,
                        required=True, help='the vlan name')
    parser.add_argument('--vlanCidr', type=int,
                        required=True, help='the vlan cidr')
    parser.add_argument('--vlanGateway', type=LowerCaseString,
                        required=False, default=None, help='the vlan gateway')
    parser.add_argument('--vlanDesc', type=LowerCaseString,
                        required=False, default=None, help='the vlan description')
    args = parser.parse_args()

    if not VlanExistsByVlanId(args.vlanId):
        print("vlan id does not already exist")
        sys.exit(1)

    if VlanExistsByVlanName(args.vlanName):
        if VlanExistsByVlanNameAndVlanId(args.vlanName, args.vlanId):
            UpdateVlan(args.vlanId, args.vlanName, args.vlanNetwork,
                       args.vlanCidr, args.vlanGateway, args.vlanDesc)
    else:
        print("vlan name already exist")
        sys.exit(1)

    sys.exit(0)


if __name__ == '__main__':
    main()
