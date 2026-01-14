# 02. API Implementation (FastAPI 사용)

01에서는 API를 구성하는 핵심 요소 중 두 가지인 SQLite 데이터베이스와, 파이썬이 데이터와 상호 작용할 수 있도록
하는 SQLAlchemy 클래스를 구현했다. 

02에서는 이 기반(01에서 만든 데이터베이스) 위에 남은 구성 요소를 구현하여 API를 완성한다. 
먼져, 요청 및 응답 메시지의 구조를 정의하는 Pydantic 스키마를 작성하고, 그 다음에 전체 API 로직을 통합해 제어하는
FastAPI 애플리케이션을 구현할 것이다.

---

02. API Implementation 에서 사용하는 소프트웨어


| 소프트웨어 이름 | 버전 | 목적 |
|---|---|---|
| FastAPI | 0 | API를 구축하기 위한 웹 프레임워크 |
| FastAPI CLI | 0 | FastAPI 명령줄 인터페이스 |
| HTTPX | 0 | 파이썬용 HTTP 클라이언트 |
| Pydantic | 2 | 데이터 유효성 검사 및 구조 정의 라이브러리 |
| Uvicorn | 0 | FastAPI 실행용 ASGI 웹 서버 |

FastAPI: API 구축을 목적으로 설계뙨 웹 프레임워크다. 
> 웹 프레임워크: 웹 애플리케이션 개발 과정에서 반복적으로 수행되는 작업을 간편하게 처리할 수 있도록 돕는 라이브러리 집합이다.

FastAPI의 주요 기능은 아래와 같다.
- HTTP 요청과 응답 처리 등 네트워크 관련 작업ㅇ르 단 몇 줄의 코드로 구현할 수 있다.
- API 명세를 설명하는 OAS 파일을 자동으로 생성하며, 이를 통해 외부 시스템과 쉽게 통합할 수 있다.
- 사용자가 직접 요청을 테스트해 볼 수 있는 대화형 API 문서를 자동으로 제공한다.
- 버전 관리, 인증 및 보안, 요청 유효성 검증 등 다양한 고급 기능을 지원한다.


HTTPX: FastAPI 기반 애플리케이션에서 비동기 처리 성능을 극대화하고, 테스트 자동화 환경에서도 필수적으로 활용되는 핵심 도구 중 하나이다.


Pydantic: API 엔드포인트를 통해 오가는 데이터 형식과 유효성을 검사하는데 도움을 준다.


Uvicorn: FastAPI와 같은 비동기 웹 프레임워크를 실행하기 위한 표준 서버로 널리 사용된다.
ASGI 명세에 따라 설계되어 FastAPI 애플리케이션을 고성능으로 실행할 수 있도록 지원한다.


아래는 이번 프로젝트에서의 각 파일들의 목적이다.

| 파일명 | 목적 |
| --- | --- |
| crud.py | 데이터베이스 쿼리를 위한 도우미 함수 |
| database.py | SQL 데이터베이스를 사용하기 위한 SQLAlchemy 설정 |
| models.py | 데이터베이스 테이블과 관련된 SQLAlchemy 클래스 정의 |
| requirements.txt | pip 패키지 관리자로 특정 버전의 라이브러리 설치에 이용 |
| test_crud.py | SQLAlchemy 파일을 단위 테스트하기 위한 파이썬 파일 |
| main.py | API 라우트를 정의하고 전체 API의 동작을 제어하는 FastAPI 파일 |
| schemas.py | API로 전달되는 요청 및 응답 데이터를 검증하는 Pydantic 클래스를 정의 |
| test_main.py | FastAPI 애플리케이션을 테스트하는 pytest 코드 파일 |



---

## 실행 흐름

다음 명령어를 실행해 새로운 라이브러리를 설치

`python -m pip install -r requirements.txt`


