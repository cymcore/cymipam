#!/usr/bin/env python3
import configparser
import os


def GetConfig(configFile):
    config = configparser.ConfigParser()
    config.read(configFile)
    return config


if os.environ.get('cymipamconf'):
    configFile = os.environ.get('cymipamconf')
else:
    configFile = 'ipamconf.ini'

config = GetConfig(configFile)

db_name = config.get('database', 'db_name')
