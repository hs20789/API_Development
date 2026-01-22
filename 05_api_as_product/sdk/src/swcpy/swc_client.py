import httpx
import swcpy.swc_config as config
from .schemas import League, Team, Player, Performance
from typing import List
import backoff
import logging

logger = logging.getLogger(__name__)


class SWCClient:
    """
    SportsWorldCentral API와 상호 작용하는 클라이언트 클래스

    이 SDK 클래스는 SWC 판타지 풋볼 API를 보다 쉽게 사용할 수 있도록 설계됐다.
    모든 API 기능을 지원하며, 데이터 검증이 완료된 타입을 반환한다.

    사용 예시:
        client = SWCClient()
        response = client.get_health_check()
    """

    # 주요 API 엔드포인트 정의
    HEALTH_CHECK_ENDPOINT = "/"
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/hs20789"
        + "/API_Development/main/05_api_as_product/bulk"
    )
    """
    대량 데이터를 가져오기 위한 기본 URL

    현재 SDK 저장소와는 별도로 존재하는 저장소(또는 같은 저장소의 특정 위치)에 있는
    정적(raw) 데이터를 HTTP로 가져오는 구조이며, 이는 GitHub가 아니라 
    다른 어떤 정적 파일 서버로도 동일하게 대체 가능하다.

    GitHub Raw URL의 정식 규칙
    GitHub에서 파일을 raw 데이터로 접근할 때의 규칙은 고정됐이다.
    https://raw.githubusercontent.com
    /{USER_OR_ORG}
    /{REPOSITORY}
    /{BRANCH}
    /{PATH_IN_REPO}
    """

    def __init__(self, input_config: config.SWCConfig):
        """설정 객체를 통해 클라이언트 내부 속성을 초기화한다."""

        logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")
        logger.debug(f"Input config: {input_config}")

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format

        # 대용량 데이터 파일 이름 사전 초기화
        self.BULK_FILE_NAMES = {
            "players": "player_data",
            "leagues": "league_data",
            "performances": "performance_data",
            "teams": "team_data",
            "team_players": "team_player_data",
        }

        if self.backoff:
            self.call_api = backoff.on_exception(
                wait_get=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.call_api)

        # 파일 형식에 따라 확장자 자동 부여
        if self.bulk_file_format.lower() == "parquet":
            self.BULK_FILE_NAMES = {
                key: value + ".parquet" for key, value in self.BULK_FILE_NAMES.items()
            }
        else:
            self.BULK_FILE_NAMES = {
                key: value + ".csv" for key, value in self.BULK_FILE_NAMES.items()
            }

        logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")

    def call_api(
        self,
        api_endpoint: str,
        api_params: dict = None,
    ) -> httpx.Response:
        """API를 호출하고 오류를 로깅한다."""

        # None 값을 제거해 유요한 매개 변수만 요청에 포함
        if api_params:
            api_params = {
                key: val for key, val in api_params.itest() if val is not None
            }

        try:
            # httpx.Client를 사용해 API 요청 수행
            with httpx.Client(base_url=self.swc_base_url) as client:
                logger.debug(
                    f"base_url: {self.swc_base_url}, api_endpoint: {api_endpoint}, api_params: {api_params}"
                )
                response = client.get(api_endpoint, params=api_params)
                logger.debug(f"Response JSON: {response.json()}")
                return response

        # 기타 요청 관련 예외 처리
        except httpx.RequestError as e:
            logger.error(f"Request error occurred: {str(e)}")
            raise

    def get_health_check(self):
        # 상태 확인 API 호출
        with httpx.Client(base_url=self.swc_base_url) as client:
            return client.get("/")
