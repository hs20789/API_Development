# 02. API Implementation (FastAPI 사용)

01에서는 API를 구성하는 핵심 요소 중 두 가지인 SQLite 데이터베이스와, 파이썬이 데이터와 상호 작용할 수 있도록
하는 SQLAlchemy 클래스를 구현했다. 

02에서는 이 기반(01에서 만든 데이터베이스) 위에 남은 구성 요소를 구현하여 API를 완성한다. 
먼져, 요청 및 응답 메시지의 구조를 정의하는 Pydantic 스키마를 작성하고, 그 다음에 전체 API 로직을 통합해 제어하는
FastAPI 애플리케이션을 구현할 것이다.

02. API Implementation 에서 사용하는 소프트웨어


| 소프트웨어 이름 | 버전 | 목적 |
|---|---|---|
| FastAPI | 0 | API를 구축하기 위한 웹 프레임워크 |
| FastAPI CLI | 0 | FastAPI 명령줄 인터페이스 |
| HTTPX | 0 | 파이썬용 HTTP 클라이언트 |
| Pydantic | 2 | 데이터 유효성 검사 및 구조 정의 라이브러리 |
| Uvicorn | 0 | FastAPI 실행용 ASGI 웹 서버 |
