import os, sys
import urllib3
import argparse
import requests, json
from tbot import telegram_post
from settings import settings
from sqlalchemy.orm import sessionmaker
from database import engine, clients

# https://ubntwiki.com/products/software/unifi-controller/api

urllib3.disable_warnings()
dbsession = sessionmaker(bind=engine)
dbsession = dbsession()

def db_insert(mac, data, notify):
    print("Inserting new client! " + mac)
    if notify:
        telegram_post("NEW CLIENT CONNECTED: {}\n\n{}".format(mac, data))
    insert = clients(mac, data)
    dbsession.add(insert)
    dbsession.commit()

def auth():
    session = requests.Session()
    myobj = {
        "username": settings['controller']['username'],
        "password": settings['controller']['password'],
    }
    url = "https://" + settings['controller']['host'] + ":" + settings['controller']['port'] + "/api/login"
    try:
        x = session.post(url, data = json.dumps(myobj), verify=False)
        return(session, x.status_code)
    except Exception as E:
        return(E)

def get_devices(session):
    if session:
        url = "https://" + settings['controller']['host'] + ":" + settings['controller']['port'] + "/api/s/default/stat/sta"
        x = session.get(url, verify=False)
        return(x.json())
    else:
        print("No database connection, exiting.")
        sys.exit(0)

def add_devices(devices, notify):
    for device in devices['data']:
        q = dbsession.query(clients).filter(clients.mac == device['mac']).first()
        if not q:
            db_insert(device['mac'], json.dumps(device), notify)
        else:
            print(device['mac'] + " already exists in db, updating data.")
            q.data = json.dumps(device)
            dbsession.commit()

def rescan():
    notify = True
    connect = auth()
    if connect[1] == 200:
        devices = get_devices(connect[0])
        if devices['meta']['rc'] == 'ok':
             add_devices(devices, notify)
        else:
            print("Cannot find any clients, exiting.")
            sys.exit(0)
    else:
        print("Error:", connect)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--notelegram', action="store_false", help="Disables Telegram notifications", required=False) # noqa : 501
    args = parser.parse_args()
    notify = args.notelegram
    connect = auth()
    if connect[1] == 200:
        devices = get_devices(connect[0])
        if devices['meta']['rc'] == 'ok':
             add_devices(devices, notify)
        else:
            print("Cannot find any clients, exiting.")
            sys.exit(0)
    else:
        print("Error:", connect)
