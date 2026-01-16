"""
pytest는 간단하고 직관적인 테스트 도구다.
pytest를 사용할 떄는 몇 가지 명명 규칙을 따라야 한다.
테스트를 포함하는 파일은 test_로 시작하거나 _test로 끝나는 이름을 가져야 하며,
파일 내에서는 test로 시작하는 이름의 함수가 자동으로 실행된다.

테스트 함수 내부에는 반드시 assert 문이 있어야 한다.
이 문이 True를 반환하면 테스트는 계속 진행되며, 모든 assert 조건이 참으로 평가되면,
테스트는 성공으로 처리되고 하나라도 assert 문이 거짓으로 평가되면
AssertionError 예외가 발생하며, 해당 테스트는 실패로 간주된다.
"""

import pytest
from datetime import date

import crud
from database import SessionLocal

test_date = date(2024, 4, 1)


@pytest.fixture(scope="function")
def db_session():
    session = SessionLocal()
    yield session
    session.close()


def test_get_player(db_session):
    player = crud.get_player(db_session, player_id=1001)
    assert player.player_id == 1001


def test_get_players(db_session):
    players = crud.get_players(
        db_session, skip=0, limit=10000, min_last_changed_date=test_date
    )
    assert len(players) == 1018


def test_get__players_by_nama(db_session):
    players = crud.get_players(db_session, first_name="Bryce", last_name="Young")
    assert len(players) == 1
    assert players[0].player_id == 2009


def test_get_all_performance(db_session):
    performances = crud.get_performances(db_session, skip=0, limit=18000)
    assert len(performances) == 17306


def test_get_new_performances(db_session):
    performances = crud.get_performances(
        db_session, skip=0, limit=18000, min_last_changed_date=test_date
    )
    assert len(performances) == 2711


def test_get_player_count(db_session):
    player_count = crud.get_player_count(db_session)
    assert player_count == 1018
