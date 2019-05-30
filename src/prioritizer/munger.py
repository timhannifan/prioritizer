import click
import pandas as pd
import numpy as np
import psycopg2 as pg

SCHEMAS = ['cleaned', 'semantic']
TABLES =['cleaned.projects','semantic.entities', 'semantic.events']

class Munger(object):
    def __init__(self, abspath=''):
        self.dbname = "timhannifan"
        self.dbhost = "127.0.0.1"
        self.dbport = 5432
        self.dbusername = "timhannifan"
        self.dbpasswd = ""
        self.conn = None
        self.abspath = abspath

    # open a connection to a psql database, using the self.dbXX parameters
    def open_connection(self):
        self.conn = pg.connect(host=self.dbhost, database=self.dbname, user=self.dbusername, port=self.dbport)

    # check whether connection is open
    def is_open(self):
            return (self.conn is not None)

    # Close any active connection to the database
    def close_connection(self):
        if self.is_open():
            self.conn.close()
            self.conn = None

    # Create any tables needed by this Client. Drop table if exists first.
    def create_tables(self):
        if self.is_open() == False:
            self.open_connection()

        cur = self.conn.cursor()

        for sch in SCHEMAS:
            schema_statement = 'create schema if not exists {};'.format(sch)
            cur.execute(schema_statement)

        for col in TABLES:
            drop_statement = 'DROP TABLE IF EXISTS {} CASCADE;'.format(col)
            cur.execute(drop_statement)

        # for command in CREATE_COMMANDS:
        #     cur.execute(command)

        cur.close()
        self.conn.commit()
        self.close_connection()

    # Add at least two indexes to the tables to improve analytic queries.
    def add_indexes(self):
        click.echo(f"Adding Indexes")
        if not self.conn:
            self.open_connection()

        cur = self.conn.cursor()

        for idx in IDXS:
            cur.execute(idx)
            self.conn.commit()

        cur.close()

    # Runs table creation and data loading
    def run(self):
        self.create_tables()

