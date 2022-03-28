import pytest

from storage import Storage


@pytest.fixture()
def storage():
    return Storage()

def test_get_empty(storage):
    with pytest.raises(KeyError):
        storage['A']

def test_set_get(storage):
    storage['A'] = '3'
    assert storage['A'] == '3'

def test_set_unset(storage):
    storage['A'] = '3'
    del storage['A']
    assert 'A' not in storage

def test_unset(storage):
    with pytest.raises(KeyError):
        del storage['A']

def test_num_equal_to(storage):
    storage['A'] = '3'
    storage['B'] = '3'
    storage['C'] = '3'
    assert storage.num_equal_to('3') == 3

def test_num_equal_to_removed(storage):
    storage['A'] = '3'
    storage['B']= '3'
    storage['C'] = '3'
    del storage['B']
    assert storage.num_equal_to('3') == 2

def test_begin(storage):
    storage.begin()
    assert storage.has_transaction()

def test_begin_commit(storage):
    storage.begin()
    storage.commit()
    assert not storage.has_transaction()

def test_begin_rollback(storage):
    storage.begin()
    storage.rollback()
    assert not storage.has_transaction()

def test_multiple_begin(storage):
    storage.begin()
    storage.begin()
    storage.commit()
    assert not storage.has_transaction()

def test_overwrite(storage):
    storage['A'] = '3'
    storage.begin()
    storage['A'] = '7'
    storage.commit()
    assert storage['A'] == '7'

def test_overwrite_rollback(storage):
    storage['A'] = '3'
    storage.begin()
    storage['A'] = '7'
    storage.rollback()
    assert storage['A'] == '3'

def test_commit_unset(storage):
    storage['A'] = '3'
    storage.begin()
    del storage['A']
    storage.commit()
    assert 'A' not in storage

def test_rollback_unset(storage):
    storage['A'] = '3'
    storage.begin()
    del storage['A']
    storage.rollback()
    assert 'A' in storage

def test_begin_num_equals(storage):
    storage['A'] = '3'
    storage.begin()
    storage['B'] = '3'
    assert storage.num_equal_to('3') == 2

def test_commit_num_equals(storage):
    storage['A'] = '3'
    storage.begin()
    storage['B'] = '3'
    storage.commit()
    assert storage.num_equal_to('3') == 2

def test_rollback_num_equals(storage):
    storage['A'] = '3'
    storage.begin()
    storage['B'] = '3'
    storage.rollback()
    assert storage.num_equal_to('3') == 1

def test_rollback_without_transaction(storage):
    with pytest.raises(RuntimeError):
        storage.rollback()

def test_rollback_without_transaction(storage):
    with pytest.raises(RuntimeError):
        storage.commit()

def test_set_unset_commit(storage):
    storage['A'] = '3'
    storage.begin()
    storage['A'] = '7'
    del storage['A']
    storage.commit()
    assert 'A' not in storage
