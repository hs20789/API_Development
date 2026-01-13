# 01. API baseline 구축하기

https://sqlite.org/download.html 에서 
SQLite 설치하기

`sqlite3 fantasy_data.db`
> 터미널에서 SQLite 데이터베이스 관리 도구를 실행하고, 그 안에서 fantasy_data.db라는 파일을 열거나 새로 만드는 역할

명령어를 치고 나면 터미널의 프롬프트 모양이 바뀐다.
```
# 입력 전 (예시)
user@computer:~$ 

# 입력 후
sqlite>
```
이제 **sqlite>** 옆에 SQL 쿼리를 입력할 수 있다.

```
sqlite> CREATE TABLE player (
(x1...> player_id INTEGER NOT NULL,
(x1...> gsis_id VARCHAR,
(x1...> first_name VARCHAR NOT NULL,
(x1...> last_name VARCHAR NOT NULL,
(x1...> position VARCHAR NOT NULL,
(x1...> last_changed_date DATE NOT NULL,
(x1...> CONSTRAINT pk_player PRIMARY KEY (player_id));
```

```
sqlite> CREATE TABLE performance (
(x1...> performance_id INTEGER NOT NULL,
(x1...> week_number VARCHAR NOT NULL,
(x1...> fantasy_points FLOAT NOT NULL,
(x1...> player_id INTEGER NOT NULL,
(x1...> last_changed_data DATE NOT NULL,
(x1...> CONSTRAINT pk_performance PRIMARY KEY (performance_id),
(x1...> CONSTRAINT fk_performance_player  
(x1...> FOREIGN KEY (player_id)
(x1...> REFERENCES player (player_id));
```

```
sqlite> CREATE TABLE league (
(x1...> league_id INTEGER NOT NULL,
(x1...> league_name VARCHAR NOT NULL,
(x1...> scoring_type VARCHAR NOT NULL,
(x1...> last_changed_date DATE NOT NULL,
(x1...> CONSTRAINT pk_league PRIMARY KEY (league_id));
```

```
sqlite> CREATE TABLE team ( 
(x1...> team_id INTEGER NOT NULL,
(x1...> team_name VARCHAR NOT NULL,
(x1...> league_id INTEGER NOT NULL,
(x1...> last_changed_date DATE NOT NULL,
(x1...> CONSTRAINT pk_team PRIMARY KEY (team_id),
(x1...> CONSTRAINT fk_team_league 
(x1...> FOREIGN KEY (league_id)
(x1...> REFERENCES league (league_id));
```

```
sqlite> CREATE TABLE team_player (
(x1...> team_id INTEGER NOT NULL,
(x1...> player_id INTEGER NOT NULL,
(x1...> last_changed_date DATE NOT NULL,
(x1...> CONSTRAINT pk_teamplayer PRIMARY KEY (team_id, player_id),
(x1...> CONSTRAINT fk_teamplayer_team FOREIGN KEY (team_id) REFERENCES team (team_id),
(x1...> CONSTRAINT fk_temaplayer_player FOREIGN KEY (player_id) REFERENCES player (player_id));
```

```
sqlite> .tables
league       performance  player       team         team_player
# 이렇게 나오면 테이블 생성 완료
```

```
sqlite> PRAGMA foreign_keys = ON;
sqlite> .mode csv
sqlite> .import --skip 1 data/player_data.csv player
sqlite> .import --skip 1 data/performance_data.csv performance
sqlite> .import --skip 1 data/league_data.csv league
sqlite> .import --skip 1 data/team_data.csv team
sqlite> .import --skip 1 data/team_player_data.csv team_player
```

여기 까지 다 했다면

`sqlite> .exit`

위의 명령어를 입력해 애플리케이션을 종료한다.
