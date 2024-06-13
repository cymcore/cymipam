#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *
import addr_add
import addr_get


def LowerCaseString(string):
    return string.lower()

def GetRecordByVlanNameAndAddrName(vlanName, addrName):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT * FROM Addr INNER JOIN Vlan ON Addr.vlan_id = Vlan.vlan_id WHERE Vlan.vlan_name = ? AND Addr.addr_name = ?''', (vlanName, addrName))
    record = cur.fetchone()
    con.close()
    if record is None:
        return None
    else:
        columns = [desc[0] for desc in cur.description]
        recordDict = dict(zip(columns, record))
        con.close()
        return recordDict


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
    
def GetAddrIpListByVlanId(vlan_id):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''SELECT addr_ip FROM Addr WHERE vlan_id = ?''', (vlan_id,))
    addr_ip = cur.fetchall()
    if addr_ip is None:
        return None
    else:
        addr_ip_list = []
        for ip in addr_ip:
            addr_ip_list.append(ip[0])
        con.close()
        return addr_ip_list
 
def GetNextOpenAddrIp(currentAddrIpList,vlanId):
    for i in range(1, 255):
        addr = f"192.168.{vlanId}.{i}"
        if addr not in currentAddrIpList:
            return addr
    return None

def main():

    parser = argparse.ArgumentParser(
        description='add an address in the database')
    parser.add_argument('--vlanName', type=LowerCaseString,
                          required=True, help='the vlan name')
    parser.add_argument('--addrName', type=LowerCaseString,
                        required=True, help='the address name')
    parser.add_argument('--addrDesc', type=LowerCaseString,
                        required=False, default=None, help='the address description')
    args = parser.parse_args()

    vlanId = GetVlanRecordByVlanName(args.vlanName)
    if vlanId is None:
        print(f"Vlan {args.vlanName} does not exist")
        sys.exit(1)
    else:
        vlanId = GetVlanRecordByVlanName(args.vlanName)['vlan_id']

    record=GetRecordByVlanNameAndAddrName(args.vlanName, args.addrName)
    if record is None:
        currentAddrIpList = GetAddrIpListByVlanId(vlanId)
        nextAddrIp = GetNextOpenAddrIp(currentAddrIpList, vlanId)

        if nextAddrIp is None:
            print("No more available addresses exist in this vlan.")
            sys.exit(1)
        addr_add.AddAddr(nextAddrIp, vlanId, args.addrName, args.addrDesc)
  
    print(addr_get.GetAddrRecordByIpName(args.addrName))
 
    sys.exit(0)


    sys.exit(0)

if __name__ == '__main__':
    main()
