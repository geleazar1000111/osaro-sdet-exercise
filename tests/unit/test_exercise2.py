import exercise2_tracker
import pytest

queue = []

def mock_load(self):
    return queue

def mock_save(self):
    return queue

class Mock_Conn:

    def commit(self):
        pass

#class Mock_Averager:
    
def insert(self, conn, item=0):
    pass
def print_stats(self, conn):
    pass


class TestPersistentQueue:

    def test_push_integer(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = [1,2,3,4]
        pq.push(1)
        
        print(pq._queue)
        assert pq._queue[-1] == 1


    def test_pop_empty_queue(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = []
        res = pq.pop()
        print(pq._queue)
        assert res == None

    def test_pop_non_empty_queue(self, monkeypatch):
        pq = exercise2_tracker.PersistentQueue("test_path")
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_load", mock_load)
        monkeypatch.setattr(exercise2_tracker.PersistentQueue, "_save", mock_save)

        pq._queue = [1]
        res = pq.pop()
        print(pq._queue)
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
        c = exercise2_tracker.Consumer([1,2,3], Mock_Conn())
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "insert", insert)
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "print_stats", print_stats)

        c._queue = [1,2,3]
        c.process()

        assert c._queue == [1,2]

    def test_process_empty_queue(self, monkeypatch):
        c = exercise2_tracker.Consumer([], Mock_Conn())
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "insert", insert)
        monkeypatch.setattr(exercise2_tracker.AveragerModel, "print_stats", print_stats)

        with pytest.raises(IndexError):
            c.process()
