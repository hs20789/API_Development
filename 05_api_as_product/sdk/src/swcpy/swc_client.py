import httpx


class SWCClient:

    def __init__(self, swc_base_url: str):
        self.swc_base_url = swc_base_url

    def get_health_check(self):
        # 상태 확인 API 호출
        with httpx.Client(base_url=self.swc_base_url) as client:
            return client.get("/")
