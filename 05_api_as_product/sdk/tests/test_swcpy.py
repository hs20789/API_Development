import pytest
from swcpy import SWCClient
from swcpy import SWCConfig
from swcpy.schemas import League, Team, Player, Performance
from io import BytesIO
import pyarrow.parquet as pq
import pandas as pd

BASE_URL = "https://api-cl-hs-b7dwdnahang7enct.japaneast-01.azurewebsites.net"


def test_health_check():
    """SDK의 상태 확인 기능을 테스트한다."""
    config = SWCConfig(swc_base_url=BASE_URL, backoff=False)
    client = SWCClient(config)
    response = client.get_health_check()
    assert response.status_code == 200
    assert response.json() == {"message": "API 상태 확인 성공"}


def test_list_leagues():
    """SDK의 리그 정보 조회 기능을 테스트한다."""
    config = SWCConfig(
        swc_base_url=BASE_URL,
        backoff=False,
    )
    client = SWCClient(config)
    leagues_response = client.list_leagues()
    # 엔드포인트가 리스트 객체를 반환하는지 검증
    assert isinstance(leagues_response, list)
    # 리스트의 각 항목이 Pydantic League 객체의 인스턴스인지 검증
    for league in leagues_response:
        assert isinstance(league, League)
    # 5개의 League 객체가 반환되는지 검증
    assert len(leagues_response) == 5


def test_bulk_player_file_parquet():
    """SDK를 이용한 Parquet 형식의 선수 데이터 대용량 다운로드 기능을 테스트"""

    config = SWCConfig(
        swc_base_url=BASE_URL,
        bulk_file_format="parquet",
    )
    client = SWCClient(config)

    player_file_parquet = client.get_bulk_player_file()

    # 파일에 올바른 레코드 수(헤더 포함)가 있는지 검증
    player_table = pq.read_table(BytesIO(player_file_parquet))

    player_df = player_table.to_pandas()
    assert len(player_df) == 1018
