#!/usr/bin/env python3
import sys
import os
import sqlite3
from get_config import *


def NewIpamDb():
    if os.path.exists(db_name):
        raise Exception("database already exists")

    else:
        con = sqlite3.connect(db_name)
        cur = con.cursor()
        cur.execute('''CREATE TABLE Vlan(vlan_id INTEGER PRIMARY KEY, vlan_name TEXT NOT NULL UNIQUE, vlan_network TEXT NOT NULL, vlan_cidr INTEGER NOT NULL, vlan_gateway TEXT, vlan_desc TEXT)''')
        cur.execute('''CREATE TABLE Addr(addr_ip TEXT PRIMARY KEY, vlan_id INTEGER NOT NULL, addr_name TEXT NOT NULL UNIQUE, addr_desc TEXT, FOREIGN KEY(vlan_id) REFERENCES Vlan(vlan_id) ON DELETE CASCADE)''')
        con.commit()
        con.close()

def main():
    try:
        NewIpamDb()
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

    sys.exit(0)

if __name__ == '__main__':
    main()
