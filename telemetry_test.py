import sqlite3
import time
import unittest

import telemetry


class TelemetryTest(unittest.TestCase):

    def setUp(self):
        self.__db_connection = sqlite3.connect('test.db')
        self.__db_connection.cursor().execute('''
            CREATE TABLE actions (
                ipAddressHash TEXT,
                userAgent TEXT,
                page TEXT,
                query TEXT,
                timestampStr TEXT
            )
        ''')
        self.__db_connection.commit()
        self.__reporter = telemetry.UsageReporter(
            lambda: sqlite3.connect('test.db'),
            min_wait=0,
            max_wait=1000,
            use_question_mark=True
        )

    def tearDown(self):
        self.__reporter.terminate()
        self.__db_connection.cursor().execute('''
            DROP TABLE actions
        ''')
        self.__db_connection.commit()

    def test_write(self):
        self.__reporter.report_usage(
            'test_ip',
            'test_agent',
            'test_page',
            'test_query'
        )

        time.sleep(2)

        cursor = self.__db_connection.cursor()
        cursor.execute('''
            SELECT * FROM actions WHERE page = 'test_page' AND query = 'test_query'
        ''')

        rows = list(cursor.fetchall())
        self.assertEquals(len(rows), 1)
