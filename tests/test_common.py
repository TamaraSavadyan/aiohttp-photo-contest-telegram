import pytest


class TestCommon:
    async def test_404(self, cli):
        response = await cli.get("/")
        assert response.status == 404
        assert await response.json() == {
            "status": "error",
            "data": {},
            "code": None,
            "message": "404: Not Found",
        }
