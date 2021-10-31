import logging
import sqlite3
from sqlite3 import Error

class Workplace():
    file_path = ''
    def set_filepath(self, filepath):
        self.file_path = filepath

    def create_workplace(self, name):
        """ Creates workplace """
        self.run_command(name, '')
        #self.init_tables(name)
        logging.info(f"Created workplace {name}")


    def run_command(self, workplace, query):
        """ runs command, workplace name and command """
        conn = None;
        try:
            conn = sqlite3.connect(f'{self.file_path}{workplace}.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
            logging.info(f'Connected to {workplace}')
            conn.execute(query) # execute
            conn.commit()
        except Error as e:
            logging.error(e)
        finally:
            if conn:
                conn.close()

    def run_script(self, workplace, query):
        """ runs script, workplace name and command """
        conn = None;
        try:
            conn = sqlite3.connect(f'{self.file_path}{workplace}.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
            logging.info(f'Connected to {workplace}')
            conn.executescript(query) # execute
            conn.commit()
        except Error as e:
            logging.error(e)
        finally:
            if conn:
                conn.close()

    # def init_tables(self, workplace):
    #     """ runs command, workplace name and command """
    #     conn = None;
    #     try:
    #         conn = sqlite3.connect(f'{self.file_path}{workplace}.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
    #         logging.info(f'Connected to {workplace}')
    #         conn.executescript('''
    #     CREATE TABLE IF NOT EXISTS phone (
    #     id integer PRIMARY KEY AUTOINCREMENT,
    #     valid text,
    #     number text,
    #     local_format text,
    #     international_format text,
    #     country_prefix text,
    #     country_code text,
    #     country_name text,
    #     location text,
    #     carrier text,
    #     line_type text );
    
    #     CREATE TABLE IF NOT EXISTS url (
    #     id integer PRIMARY KEY AUTOINCREMENT,
    #     ip text );

    #     CREATE TABLE IF NOT EXISTS google (
    #     id integer PRIMARY KEY AUTOINCREMENT,
    #     url text );

    #     CREATE TABLE IF NOT EXISTS ip (
    #     id integer PRIMARY KEY AUTOINCREMENT,
    #     query text,
    #     status text,
    #     country text,
    #     countryCode text,
    #     region text,
    #     regionName text,
    #     city text,
    #     zip text,
    #     lat text,
    #     lon text,
    #     timezone text,
    #     isp text,
    #     org text,
    #     as_ text,
    #     success text,
    #     message text,
    #     fraud_score text,
    #     is_crawler text,
    #     mobile text,
    #     host text,
    #     proxy text,
    #     vpn text,
    #     tor text,
    #     active_vpn text,
    #     active_tor text,
    #     recent_abuse text,
    #     bot_status text
    #     );

    #     CREATE TABLE IF NOT EXISTS email (
    #     id integer PRIMARY KEY AUTOINCREMENT,
    #     emailAddress text,
    #     formatCheck text,
    #     smtpCheck text,
    #     dnsCheck text,
    #     freeCheck text,
    #     disposableCheck text,
    #     catchAllCheck text,
    #     mxRecords text,db
    #     auditCreatedDate text,
    #     auditUpdatedDate text);
    #     ''')
    #         conn.commit()
    #     except Error as e:
    #         logging.error(e)
    #     finally:
    #         if conn:
    #             conn.close()

    
    def create_table(self, workplace, name, columns):
        columns = columns | { 'id': 'INTEGER PRIMARY KEY AUTOINCREMENT' }
        query = f'CREATE TABLE {name} ('
        for column in columns: 
            query += '\n' + str(column) + ' ' + str(columns[column] + ',')
        self.run_command(workplace, query[:-1] + ');') 
        logging.info(f'Created {name} table in {workplace}')


    def delete_table(self, workplace, name):
        self.run_command(workplace, f'DROP TABLE {name};')
        logging.info(f'Dropped {name} table in {workplace}')

        
    def add_muiltple_rows(self, workplace, name, values):
        """ given workplace name string and list of tuples of rows to add"""
        conn = None;
        try:
            conn = sqlite3.connect(f'{self.file_path}{workplace}.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
            logging.info(f'Connected to {workplace}')
            cursor=conn.execute(f"SELECT * FROM {name};")
            names = [description[0] for description in cursor.description]
            logging.info(f'Connected to {workplace}')
            # format string of names eg. ('name', 'name')
            names.remove('id')
            names_string = "("
            for index, col_name in enumerate(names):
                names_string += f"'{col_name}'"
                if index < len(names) - 1:
                    names_string += ','
            names_string += ')'
            conn.executemany(f'INSERT INTO {name} VALUES{names_string};',values);
            conn.commit()
        except Error as e:
            logging.error(e)
        finally:
            if conn:
                conn.close()


    def add_row(self, workplace, name, values):
        conn = None;
        try:
            conn = sqlite3.connect(f'{self.file_path}{workplace}.sqlite', detect_types=sqlite3.PARSE_DECLTYPES)
            logging.info(f'Connected to test')
            # get list of names in table
            cursor=conn.execute(f"SELECT * FROM {name};")
            names = [description[0] for description in cursor.description]
            logging.info(f'Connected to {workplace}')
            # format string of names eg. ('name', 'name')
            names.remove('id')
            names_string = "("
            for index, col_name in enumerate(names):
                names_string += f'"{col_name}"'
                if index < len(names) - 1:
                    names_string += ','
            names_string += ')'
            # format values
            values_string = "("
            for index, value in enumerate(values):
                values_string += f'"{value}"'
                if index < len(values) - 1:
                    values_string += ','
            values_string += ')'
            conn.execute(f"""
            INSERT INTO {name} {names_string}
            VALUES{values_string}; 
        """) # execute
            conn.commit()
            logging.info(f'Added row to {workplace}')
        except Error as e:
            logging.error(e)
        finally:
            if conn:
                conn.close()


    def delete_row(self, workplace, name, id):
        self.run_command(workplace, f'DELETE from {name} where id = {id};')
        logging.info(f'Dropped {id} row in {name} table')