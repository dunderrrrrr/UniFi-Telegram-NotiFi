settings = {
    "system": {
        "dblocation": "/home/user/path/db/sqlite.db" # Full path to database location
    },
    "controller": {
        "host": "192.168.1.1", # Unifi controller IP
        "port": "8443", # Unifi controller port
        "username": "admin", # Unifi username (highly recommended using a read-only account)
        "password": "p4ssw0rd" # Unifi account password
    },
    "telegram": {
        "url": "https://api.telegram.org/bot", # Telegram API url
        "token": "1234567890:xxxxxxx", # Telegram bot token from Botfather
        "groupid": "1234567890", # Telegram message id from https://api.telegram.org/bot<token>/getUpdates, see readme for more information.
        "test_msg_enable": True # Enable or disable test-message ability from webgui (Default: True)
    }
}
