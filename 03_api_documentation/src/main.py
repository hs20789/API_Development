"""FastAPI 컨트롤러"""

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from datetime import date

import crud, schemas
from database import SessionLocal

api_description = """
이 API는 SportWorldCentral(SWC) 판타지 풋볼 API의 정보를 읽기 전용으로 제공한다.
제공되는 엔드포인트는 아래와 같다.

## 분석(analytics)
API의 상태 및 리그, 팀, 선수 수에 대한 정보를 제공한다.

## 선수(players)
NFL 선수 목록을 조회하거나, 특정 player_id를 이용해 개별 선수 정보를 제공한다.

## 점수(scoring)
NFL 선수의 경기 성적과 해당 성적을 기반으로 한 SWC 리그 판타지 점수를 제공한다.

## 멤버심(membership)
SWC 판타지 풋볼 리그 전체와 각 리그에 속한 팀에 대한 정보를 제공한다.
"""

# OpenAPI 명세에 추가 세부 정보가 추가된 FastAPI 생성자
app = FastAPI(
    description=api_description,
    title="Sports World Central(SWC) Fantasy Football API",
    version="0.1",
)


# 종속성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/",
    summary="SWC 판타지 풋볼 API가 동작 중인지 확인합니다.",
    description="API가 정상적으로 실행 중인지 확인하기 위한 엔드포인트입니다. 다른 API를 호출하기 전에 먼저 호출하여 서버 상태를 점검할 수 있습니다.",
    response_description="API가 실행 중이면 성공 메시지를 포함한 JSON 객체를 반환합니다.",
    operation_id="v0_health_check",
    tags=["analytics"],
)
async def root():
    return {"message": "API 상태 확인 성공"}


@app.get(
    "/v0/players/",
    response_model=list[schemas.Player],
    summary="요청 파라미터 조건에 맞는 SWC 선수 목록을 조회합니다.",
    description=(
        "SWC 선수 목록을 조회하는 엔드포인트입니다. 여러 파라미터로 선수를 필터링할 수 있습니다. "
        "이름은 유일하지 않을 수 있으므로(동명이인 가능) 주의하세요. "
        "skip과 limit를 사용해 페이지네이션을 수행합니다. "
        "또한 Player ID는 내부 식별자이며 순서가 보장되지 않으므로, 개수 계산이나 순번 기반 로직에 사용하지 마세요."
    ),
    response_description="SWC 판타지 풋볼에 등록된 NFL 선수 목록을 반환합니다(팀에 소속되지 않은 선수도 포함될 수 있습니다).",
    operation_id="v0_get_players",
    tags=["players"],
)
def read_players(
    skip: int = 0,
    limit: int = 100,
    minimum_last_changed_date: date = None,
    first_name: str = None,
    last_name: str = None,
    db: Session = Depends(get_db),
):
    players = crud.get_players(
        db,
        skip=skip,
        limit=limit,
        min_last_changed_date=minimum_last_changed_date,
        first_name=first_name,
        last_name=last_name,
    )
    return players


@app.get(
    "/v0/players/{player_id}",
    response_model=schemas.Player,
    summary="SWC 내부 선수 ID로 단일 선수 정보를 조회합니다.",
    description=(
        "v0_get_players와 같은 다른 API 호출에서 얻은 SWC Player ID를 사용해 특정 선수를 조회할 수 있습니다."
    ),
    response_description="선택한 NFL 선수 1명의 정보를 반환합니다.",
    operation_id="v0_get_players_by_player_id",
    tags=["players"],
)
def get_read_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다!")
    return player


@app.get(
    "/v0/performances/",
    response_model=list[schemas.Performance],
    summary="요청 파라미터 조건에 맞는 선수 주간 퍼포먼스(성적) 목록을 조회합니다.",
    description=(
        "SWC에서 선수들의 주간 퍼포먼스(예: 판타지 포인트 포함) 목록을 조회하는 엔드포인트입니다. "
        "skip과 limit로 페이지네이션을 수행할 수 있습니다. "
        "Performance ID는 내부 식별자이며 순차성이 보장되지 않으므로, 카운팅이나 순번 기반 로직에 사용하지 마세요."
    ),
    response_description="여러 선수의 주간 스코어링 퍼포먼스 목록을 반환합니다.",
    operation_id="v0_get_performances",
    tags=["scoring"],
)
def read_performances(
    skip: int = 0,
    limit: int = 100,
    minimum_last_changed_date: date = None,
    db: Session = Depends(get_db),
):
    performances = crud.get_performances(
        db, skip=skip, limit=limit, min_last_changed_date=minimum_last_changed_date
    )
    return performances


@app.get(
    "/v0/leagues/{league_id}",
    response_model=schemas.League,
    summary="리그 ID로 단일 리그 정보를 조회합니다.",
    description="사용자가 제공한 리그 ID와 일치하는 리그 1개를 조회하는 엔드포인트입니다.",
    response_description="선택한 SWC 리그 정보를 반환합니다.",
    operation_id="v0_get_league_by_league_id",
    tags=["membership"],
)
def read_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="리그를 찾을 수 없습니다!")
    return league


@app.get(
    "/v0/leagues/",
    response_model=list[schemas.League],
    summary="요청 파라미터 조건에 맞는 SWC 판타지 풋볼 리그 목록을 조회합니다.",
    description=(
        "SWC 판타지 풋볼 리그 목록을 조회하는 엔드포인트입니다. "
        "skip과 limit로 페이지네이션을 수행할 수 있습니다. "
        "리그 이름은 유일하지 않을 수 있습니다. "
        "League ID는 내부 식별자이며 순차성이 보장되지 않으므로, 카운팅이나 순번 기반 로직에 사용하지 마세요."
    ),
    response_description="SWC 판타지 풋볼 웹사이트에 등록된 리그 목록을 반환합니다.",
    operation_id="v0_get_leagues",
    tags=["membership"],
)
def read_leagues(
    skip: int = 0,
    limit: int = 100,
    minimum_last_changed_date: date = None,
    league_name: str = None,
    db: Session = Depends(get_db),
):
    leagues = crud.get_leagues(
        db,
        skip=skip,
        limit=limit,
        min_last_changed_date=minimum_last_changed_date,
        league_name=league_name,
    )
    return leagues


@app.get(
    "/v0/teams/",
    response_model=list[schemas.Team],
    summary="요청 파라미터 조건에 맞는 SWC 판타지 풋볼 팀 목록을 조회합니다.",
    description=(
        "SWC 판타지 풋볼 팀 목록을 조회하는 엔드포인트입니다. "
        "skip과 limit로 페이지네이션을 수행할 수 있습니다. "
        "팀 이름은 유일하지 않을 수 있습니다. "
        "다른 API(예: v0_get_players)에서 얻은 Team ID를 이 엔드포인트 결과의 Team ID와 매칭하여 사용할 수 있습니다. "
        "Team ID는 내부 식별자이며 순차성이 보장되지 않으므로, 카운팅이나 순번 기반 로직에 사용하지 마세요."
    ),
    response_description="SWC 판타지 풋볼 웹사이트에 등록된 팀 목록을 반환합니다.",
    operation_id="v0_get_teams",
    tags=["membership"],
)
def read_teams(
    skip: int = 0,
    limit: int = 0,
    minimum_last_changed_date: date = None,
    team_name: str = None,
    league_id: int = None,
    db: Session = Depends(get_db),
):
    teams = crud.get_teams(
        db,
        skip=skip,
        limit=limit,
        min_last_changed_date=minimum_last_changed_date,
        team_name=team_name,
        league_id=league_id,
    )
    return teams


@app.get(
    "/v0/counts/",
    response_model=schemas.Counts,
    summary="SWC 판타지 풋볼의 리그·팀·선수 개수를 집계해 반환합니다.",
    description=(
        "SWC 판타지 풋볼의 리그 수, 팀 수, 선수 수를 집계하는 엔드포인트입니다. "
        "v0_get_leagues, v0_get_teams, v0_get_players의 skip/limit 페이지네이션과 함께 사용하여 "
        "전체 규모를 파악하는 용도로 사용할 수 있습니다. "
        "개수 계산이 필요할 때 다른 API를 반복 호출하기보다 이 엔드포인트를 사용하는 것을 권장합니다."
    ),
    response_description="리그/팀/선수 개수를 담은 집계 결과를 반환합니다.",
    operation_id="v0_get_counts",
    tags=["analytics"],
)
def get_count(db: Session = Depends(get_db)):
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count=crud.get_team_count(db),
        player_count=crud.get_player_count(db),
        performace_count=crud.get_performance_count(db),
    )
    return counts
