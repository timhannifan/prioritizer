import click
import psycopg2 as pg
import csv

TABLES = ['raw', 'raw_projects']
IDXS = []
CREATE_COMMANDS = [
            """
            CREATE TABLE raw (
                projectid VARCHAR(50) PRIMARY KEY UNIQUE,
                teacher_acctid VARCHAR,
                schoolid VARCHAR(50),
                school_ncesid DECIMAL,
                school_latitude DECIMAL,
                school_longitude DECIMAL,
                school_city VARCHAR(50),
                school_state VARCHAR(2),
                school_metro VARCHAR(50),
                school_district VARCHAR(200),
                school_county VARCHAR(50),
                school_charter VARCHAR(50),
                school_magnet VARCHAR(50),
                teacher_prefix VARCHAR(50),
                primary_focus_subject VARCHAR(50),
                primary_focus_area VARCHAR(50),
                secondary_focus_subject VARCHAR(50),
                secondary_focus_area VARCHAR(50),
                resource_type VARCHAR(50),
                poverty_level VARCHAR(50),
                grade_level VARCHAR(50),
                total_price_including_optional_support DECIMAL,
                students_reached INT,
                eligible_double_your_impact_match VARCHAR(2),
                date_posted TIMESTAMP,
                datefullyfunded TIMESTAMP
                )
            """,
            """
            CREATE TABLE raw_projects (
                projectid VARCHAR(50) PRIMARY KEY UNIQUE,
                teacher_acctid VARCHAR,
                -- schoolid VARCHAR(50),
                -- school_ncesid DECIMAL,
                -- school_latitude DECIMAL,
                -- school_longitude DECIMAL,
                school_city VARCHAR(50),
                school_state VARCHAR(2),
                -- school_metro VARCHAR(50),
                -- school_district VARCHAR(200),
                school_county VARCHAR(50),
                -- school_charter VARCHAR(50),
                -- school_magnet VARCHAR(50),
                -- teacher_prefix VARCHAR(50),
                primary_focus_subject VARCHAR(50),
                -- primary_focus_area VARCHAR(50),
                -- secondary_focus_subject VARCHAR(50),
                -- secondary_focus_area VARCHAR(50),
                resource_type VARCHAR(50),
                poverty_level VARCHAR(50),
                grade_level VARCHAR(50),
                total_price_including_optional_support DECIMAL,
                students_reached INT,
                -- eligible_double_your_impact_match VARCHAR(2),
                date_posted TIMESTAMP,
                datefullyfunded TIMESTAMP
                )
            """
            ]
BULK_INSERTS = [
    """
    INSERT INTO raw_projects (projectid,teacher_acctid,school_city,school_state,school_county,primary_focus_subject,resource_type,poverty_level,grade_level,total_price_including_optional_support,students_reached,date_posted,datefullyfunded)
    SELECT DISTINCT projectid,teacher_acctid,school_city,school_state,school_county,primary_focus_subject,resource_type,poverty_level,grade_level,total_price_including_optional_support,students_reached,date_posted,datefullyfunded
    FROM raw;
    """]

class Client:
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

        for col in TABLES:
            drop_statement = 'DROP TABLE IF EXISTS {} CASCADE;'.format(col)
            cur.execute(drop_statement)

        for command in CREATE_COMMANDS:
            cur.execute(command)

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

    # This function will bulk load the data using copy
    def bulk_load_file(self, file_path):

        click.echo(f"Bulk load file from %s" % file_path)
        if self.is_open() == False:
            self.open_connection()

        cur = self.conn.cursor()

        drop_statement = 'DROP TABLE IF EXISTS {};'.format('bulk_temp')
        cur.execute(drop_statement)

        copy_sql = """
           COPY raw FROM stdin WITH CSV HEADER
           DELIMITER as ','
           """

        with open(file_path, 'r') as f:
            try:
                reader = csv.reader(f, delimiter=',')

                cur.copy_expert(sql=copy_sql, file=f)
                for insert in BULK_INSERTS:
                    cur.execute(insert)
                self.conn.commit()
                cur.close()

            except (Exception, pg.DatabaseError) as error:
                print(error)
            finally:
                if self.conn is not None:
                    cur.close()
                self.close_connection()


    # Runs table creation and data loading
    def run(self, abspath):
        self.create_tables()
        self.bulk_load_file(abspath)
