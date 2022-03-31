# script contains main functions to save to sqlite3 workplace/database

import logging
import sqlite3
from sqlite3 import Error

__author__ = 'Harry Ludemann'
__version__ = '0.1.0'

class Workplace():
    file_path: str = ''
    name: str = 'N/A'
    
    def __init__(self, filepath: str, name: str):
        self.file_path = filepath
        self.name = name

    def set_filepath(self, filepath: str):
        self.file_path = filepath

    def create_workplace(self, name: str):
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


    def save_to_workplace(self, context: dict, plugin_name: str) -> None:
        """ Saves context dict to given plugins names table in current workplace,
        either adds all vars in context to array, or if item is array creates row of that array """
        values = []
        added_row = False
        first_var = True
        for name in context:
            if first_var and type(context[name]) == list: # if first var is list, add all vars in list
                added_row = True
                for item in context[name]:
                    self.add_row(self.name, plugin_name, [item])
            else:
                values.append(context[name]) # else add value
            first_var = False
        if not added_row:
            self.add_row(self.name, plugin_name, values)