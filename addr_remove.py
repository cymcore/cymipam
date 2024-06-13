#!/usr/bin/env python3
import sys
import argparse
import sqlite3
from get_config import *


def LowerCaseString(string):
    return string.lower()


def AddrExistsByIp(addr_ip):
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


def AddrExistsByName(addr_name):
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


def RemoveAddrByAddrName(addr_name):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''DELETE FROM Addr WHERE addr_name = ?''', (addr_name,))
    con.commit()
    con.close()
    print("address removed successfully")


def RemoveAddrByAddr(addr_ip):
    con = sqlite3.connect(db_name)
    con.execute('PRAGMA foreign_keys = ON')
    cur = con.cursor()
    cur.execute('''DELETE FROM Addr WHERE addr_ip = ?''', (addr_ip,))
    con.commit()
    con.close()
    print("address removed successfully")


def main():
    parser = argparse.ArgumentParser(
        description='remove an address from the database')
    parser.add_argument('--addrIp', type=LowerCaseString,
                        required=False, help='the address ip')
    parser.add_argument('--addrName', type=LowerCaseString,
                        required=False, help='the address name')
    args = parser.parse_args()

    if len(sys.argv) < 2:
        print("provide one of the two optional arguments, --addrIp or --addrName")
        sys.exit(1)

    if args.addrIp and AddrExistsByIp(args.addrIp):
        addr = RemoveAddrByAddr(args.addrIp)
        sys.exit(0)

    if args.addrName and AddrExistsByName(args.addrName):
        addr = RemoveAddrByAddrName(args.addrName)
        sys.exit(0)

    print("addr does not exist")
    sys.exit(1)


if __name__ == '__main__':
    main()
