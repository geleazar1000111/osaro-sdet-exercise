import exercise2_tracker
import pytest


def mock_load(self):
    pass


def mock_save(self):
    pass


def insert(self, conn, item=0):
    pass


def print_stats(self, conn):
    pass


class MockConn:

    def commit(self):
        pass


class TestPersistentQueue:

    def test_push_integer(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = [1,2,3,4]
        pq.push(1)
        
        assert pq._queue[-1] == 1


    def test_pop_empty_queue(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = []
        res = pq.pop()
        assert res == None

    def test_pop_non_empty_queue(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = [1]
        res = pq.pop()
        assert res == 1


class TestAveragerModel:

    def test_insert_integer(self):
        pass

    def test_insert_non_integer(self):
        pass

    def test_count(self):
        pass

    def test_sum(self):
        pass


class TestConsumer:

    def test_process_nonempty_queue(self, monkeypatch):
        c = exercise2_tracker.Consumer([1,2,3], MockConn())
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "insert", insert)
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "print_stats", print_stats)

        c._queue = [1,2,3]
        c.process()

        assert c._queue == []

    def test_process_empty_queue(self, monkeypatch):
        c = exercise2_tracker.Consumer([], MockConn())
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "insert", insert)
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "print_stats", print_stats)

        with pytest.raises(IndexError):
            c.process()
