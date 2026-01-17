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


@app.get("/", tags=["analytics"])
async def root():
    return {"message": "API 상태 확인 성공"}


@app.get("/v0/players/", response_model=list[schemas.Player], tags=["player"])
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


@app.get("/v0/players/{player_id}", response_model=schemas.Player, tags=["player"])
def get_read_player(player_id: int, db: Session = Depends(get_db)):
    player = crud.get_player(db, player_id=player_id)
    if player is None:
        raise HTTPException(status_code=404, detail="선수를 찾을 수 없습니다!")
    return player


@app.get(
    "/v0/performances/", response_model=list[schemas.Performance], tags=["scoring"]
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


@app.get("/v0/leagues/{league_id}/", response_model=schemas.League, tags=["membership"])
def read_league(league_id: int, db: Session = Depends(get_db)):
    league = crud.get_league(db, league_id=league_id)
    if league is None:
        raise HTTPException(status_code=404, detail="리그를 찾을 수 없습니다!")
    return league


@app.get("/v0/leagues/", response_model=list[schemas.League], tags=["membership"])
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


@app.get("/v0/teams/", response_model=list[schemas.Team], tags=["membership"])
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


@app.get("/v0/counts/", response_model=schemas.Counts, tags=["analytics"])
def get_count(db: Session = Depends(get_db)):
    counts = schemas.Counts(
        league_count=crud.get_league_count(db),
        team_count=crud.get_team_count(db),
        player_count=crud.get_player_count(db),
        performace_count=crud.get_performance_count(db),
    )
    return counts
