import sqlite3
import sys
from notifier.notifier import Notifier

# IMPORTANT:
# no protection against sql injection here (I did not find a way to parameterize the table names in the queries...)
# if you do not let anybody untrusted edit the config file "sitesToCheckConfig.json", this shouldn't be a problem though
class SqliteconnHandler:

    def __init__(self, filename: str, notify: bool, logger: object, notifier: Notifier = None):
        self.filename = filename
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.notify = notify
        self.notifier = notifier
        self.logger = logger

    def create_table_if_not_exists(self, site: str):
        try:
            self.c.execute('CREATE TABLE IF NOT EXISTS ' + site + '(element text)')
            self.conn.commit()
        except Exception as e:
            exception = str(sys.exc_info()[0])
            self.logger.log.exception("Could not create table {} in sql file because of: {}".format(site, exception))

    def close_connection(self):
        self.conn.close()

    def insert_element_if_not_exists_into_table(self, element: str, site: str):

        try:
            self.c.execute('SELECT * FROM ' + site + ' WHERE element=\"' + element+"\"")
            entry = self.c.fetchone()
            # only insert when entry does not yet exist
            if entry is None:
                self.c.execute('INSERT INTO ' + site + ' (element) VALUES (' + '"' + element + '")')
                self.conn.commit()
                # only notify when it is stated that way in config file
                if self.notify:
                    self.notifier.notify_about_new_element_via_pushover(site, element)
        except Exception as e:
            exception = str(sys.exc_info()[0])
            self.logger.log.exception("Could not insert element {} into table {} in sql file because of: {}".format(element, site, exception))
