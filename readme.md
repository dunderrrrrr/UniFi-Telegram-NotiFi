![screenshot](https://i.imgur.com/Dkc5LdK.png "screenshot")

# UniFi Telegram NotiFi
Get notified on Telegram if a new or unknown client connects to your network.

# How it works
`update.py` makes API requests to your controller and is querying `https://yourcontroller:8443/api/s/default/stat/sta` which contains a list of all _active_ clients on the site. These clients are stored in a sqlite3 database, `db/sqlite.db`. When the script discovers a new client not already stored in the database, a [Telegram](https://telegram.org/) message will be sent to you with all available client data. If you choose to delete a client it will be removed from the database. If the client reconnects you'll be notified again.

This script has been tested on UniFi Controller version 6.1.71, installed on Ubuntu 20.04 but will probably work with other versions aswell.  

[API Documentation](https://ubntwiki.com/products/software/unifi-controller/api)  
[Screenshot](https://i.imgur.com/Dkc5LdK.png)  
[Install Ubiquiti Unifi Controller on Ubuntu 20.04](https://gist.github.com/dunderrrrrr/67fa6b11c6ba0048ddc16b0cd3d8089f)  

# Installation
1. Clone this repo, create [virtualenv](https://gist.github.com/dunderrrrrr/c3a6d5cba1b7320d6835b0fe995f5e6b) (optional but recommended) and install requirements. Also create log folder.
```
$ mkvirtualenv unifi-monitor
$ pip install -r requirements.txt
$ sudo mkdir /var/log/unifi-telegram-notifi
```
2. Copy `settings.sample.py` and edit settings.
```
$ cp settings.sample.py settings.py
```
3. Create database
```
$ python database.py
```
4. Insert existing clients to database. You can choose if you want a Telegram message for each client or not. If you have alot of clients connected it's recommended to apply the notelegram parameter (or you will recieve alot of messages)
```
$ python update.py
$ python update.py --notelegram
```
5. The database should now be created and there should also be data inserted. You can now run the webgui.
```
$ python web.py
```
The webserver is listening by default on `http://serverip:5000`.  
If everything looks fine you should schedule a cronjob triggering `update.py`.
```
$ sudo crontab -e
```
```
* * * * * /home/user/virtualenvs/virtualenv_name/bin/python3.8 /home/user/path/unifi-telegram-notifi/update.py >> /var/log/unifi-telegram-notify/cron.log 2>&1
```
# Telegram settings
Message [@Botfather](https://telegram.me/botfather) on Telegram and set up your bot. Make sure you save your token.

To get your Group ID (needs to be set in `settings.py`):  
1. When your bot is created, send a random message to your bot.  
2. Visit `https://api.telegram.org/bot<YourBOTToken>/getUpdates`.  
3. Use the "id" of the "chat" object to send your messages.  

More information: [https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id](https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id)  
Pull requests are welcome.
