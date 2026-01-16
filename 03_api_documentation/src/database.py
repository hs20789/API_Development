"""데이터베이스 구성"""

# SQLAlchemy 전체를 한 번에 가져올 수도 있지만, 여러 라이브러리 간 중복 함수로 인해 발생할 수 있는
# 충돌을 방지하기 위해 필요한 함수만 명시적으로 가져오는 것이 권장된다.

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./fantasy_data.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
