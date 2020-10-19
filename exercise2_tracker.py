"""
This system contains a "producer" that populates a queue and a "consumer" that asynchronously 
reads from a queue and inserts integer records into a database. The average of these records
is reported on a regular interval"""
import logging
import os
import pickle
import sqlite3
import sys
import time

logger = logging.getLogger('averager')

def with_persistence(func):
    """Decorator for write actions in PersistentQueue"""
    def inner(self, *args, **kwargs):
        self._load()
        result = func(self, *args, **kwargs)
        self._save()
        return result

    return inner

class PersistentQueue:
    """Queue that is written and read from disk"""
    def __init__(self, file_path):
        self._file_path = file_path
        self._queue = []

    @with_persistence
    def push(self, item):
        """Adds an element to the end of the queue and saves the queue to disk"""
        if not isinstance(item, list):
            item = [item]

        self._queue += item

    @with_persistence
    def pop(self):
        """Removes the first element from the queue and returns it.
        Returns None if the queue is empty. 
        Saves updated queue to disk"""
        if not len(self._queue):
            return None

        item = self._queue.pop(0)
        return item

    def _load(self):
        """Reads the queue from disk and loads it into memory"""
        if os.path.exists(self._file_path):
            self._queue = pickle.load(open(self._file_path, "rb"))

    def _save(self):
        """Saves the queue to disk"""
        pickle.dump( self._queue, open(self._file_path, "wb" ) )

class AveragerModel:
    """Facilitates database interactions and computes statistics regarding the data"""
    @classmethod
    def insert(cls, conn, count):
        """Inserts an integer into the counts table"""
        query = f"INSERT INTO counts (val) VALUES('{int(count)}')"
        conn.execute(query)

    @classmethod
    def sum(cls, conn):
        """Computes the sum of all values in the counts tables"""
        query = "SELECT SUM(val) AS sum FROM counts"
        cursor = conn.execute(query)
        row = cursor.fetchone()
        return row[0] or 0

    @classmethod
    def count(cls, conn):
        """Computes the number of records in the counts table"""
        query = "SELECT COUNT(*) AS sum FROM counts"
        cursor = conn.execute(query)
        row = cursor.fetchone()
        return row[0] or 0

    @classmethod
    def print_stats(cls, conn):
        """Logs the count, sum, and average of the records in the counts table"""
        item_sum = cls.sum(conn)
        item_count = cls.count(conn)
        average = item_sum / item_count if item_count else 0
        logger.info(f"STATS: Count:{item_count} Sum:{item_sum} Average:{average}")

class Consumer:
    """Periodically processes queue entries"""
    def __init__(self, queue, conn, interval=1):
        self._queue = queue
        self._interval = interval
        self._conn = conn

    def process(self):
        """Transfers all elements of the queue to the database and prints updated stats"""
        item = self._queue.pop()
        while item:
            AveragerModel.insert(self._conn, item)
            item = self._queue.pop()

        self._conn.commit()
        AveragerModel.print_stats(self._conn)

    def start(self):
        """Runs until keyboard interrupt. Periodically process the queue"""
        try:
            while True:
                self.process()
                time.sleep(self._interval)
        except KeyboardInterrupt:
            logger.info("Exiting")
        finally:
            self._conn.commit()
            self._conn.close()

def initialize_db(filename):
    """Returns a sqlite database connection. Initializes the counts table if it does not exist"""
    create_table = not os.path.exists(filename)
    conn = sqlite3.connect(filename)

    if create_table:
        logging.info("Creating database")
        conn.execute('CREATE TABLE counts (val int NOT NULL);')

    return conn

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='''Produces and consumes numbers that are averaged''')
    parser.add_argument('--consumer', dest='is_consumer', action='store_true', help='Runs the consumer')
    parser.add_argument('--produce', dest='produce', type=int, nargs=1, help='Adds an integer to the queue')
    args = parser.parse_args()

    logging.basicConfig(level = logging.INFO)

    queue = PersistentQueue('./counts.queue')
    if args.is_consumer:
        conn = initialize_db('./counts.db')
        consumer = Consumer(queue, conn)
        consumer.start()
    elif args.produce:
        queue.push(args.produce[0])
        logger.info(f"Produced: {args.produce[0]}")
    else:
        parser.print_help(sys.stderr)
        logger.error("Invalid options. Must supply --consumer or --produce")
        exit(1)
