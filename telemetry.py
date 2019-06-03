"""Utility to log usage statistics.

----

Copyright 2019 Data Driven Empathy LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
associated documentation files (the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge, publish, distribute,
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES
OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import datetime
import hashlib
import multiprocessing
import random
import time


INSERT_TEMPLATE = '''INSERT INTO actions (ipAddressHash, userAgent, page, query, timestampStr) VALUES (?, ?, ?, ?, ?)'''


def run_worker_logic(task_queue, db_connection_generator, min_wait, max_wait, use_question_mark):
    """Run worker process logic.

    Args:
        task_queue: Queue to control records to be written.
        db_connection_generator: Function taking no arguments and returning DB API v2 compliant
            connection interface through which the record should be created.
        min_wait: Minimum millisecond delay before checking for new tasks.
        max_wait: Maximum millisecond delay before checking for new tasks.
        use_question_mark: Flag indicating if question marks should be used in insert template.
            If true, uses ?. If false, uses %s.
    """

    if use_question_mark:
        insert_sql = INSERT_TEMPLATE
    else:
        insert_sql = INSERT_TEMPLATE.replace('?', '%s')

    def execute_task(task):
        """Inner closure that executes a single task.

        Args:
            task: Dictionary describing the task to exeucte.
        """
        db_connection = db_connection_generator()
        cursor = db_connection.cursor()

        ip_address = task['ipAddress']
        user_agent = task['userAgent']
        page = task['page']
        query = task['query']
        timestamp_str = task['timestampStr']

        hashable_str = ip_address + user_agent
        ip_address_hash = hashlib.sha224(hashable_str.encode('utf-8')).hexdigest()

        cursor.execute(
            insert_sql,
            (ip_address_hash, user_agent, page, query, timestamp_str)
        )

        db_connection.commit()

    while True:
        task = task_queue.get()

        if task is None:
            time.sleep(random.randint(min_wait, max_wait) / 1000)
        else:
            if task['end']:
                return

            execute_task(task)

class UsageReporter:
    """Utility which runs a reporting subprocess for user actions."""

    def __init__(self, db_connection_generator, min_wait=1000, max_wait=5000,
            use_question_mark=False):
        """Create a new reporter.

        Args:
            db_connection_generator: Function taking no arguments and returning DB API v2 compliant
                connection interface through which the record should be created.
            min_wait: Minimum delay before processing new tasks.
            min_wait: Maximum delay before processing new tasks.
            Flag indicating if question marks should be used in insert template.
                If true, uses ?. If false, uses %s.
        """
        self.__db_connection = db_connection_generator()

        task_queue = multiprocessing.Queue()
        self.__queue = task_queue

        self.__inner_process = multiprocessing.Process(
            target=run_worker_logic,
            args=(task_queue, db_connection_generator, min_wait, max_wait, use_question_mark)
        )

        self.__inner_process.start()

    def report_usage(self, ip_address, user_agent, page, query):
        """Asynchoronously report a user action within the application.

        Args:
            ip_address: String IP address to be hashed for creating this record.
            user_agent: String user agent which will be used as sald for the ip_address hash.
            page: String page name.
            query: String query or empty if no query.
        """
        self.__queue.put({
            'ipAddress': ip_address,
            'userAgent': user_agent,
            'page': page,
            'query': query,
            'timestampStr': datetime.datetime.utcnow().isoformat(),
            'end': False
        })

    def terminate(self):
        """Terminate the inner subprocess"""
        self.__queue.put({'end': True})
        self.__inner_process.join()
        self.__queue.close()
        self.__queue.join_thread()
