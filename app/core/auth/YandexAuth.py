import httpx
from fastapi import HTTPException

from core.config.Environment import get_environment_variables

env = get_environment_variables()


async def get_yandex_user(code: str):
    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            "https://oauth.yandex.ru/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "client_id": env.YANDEX_CLIENT_ID,
                "client_secret": env.YANDEX_CLIENT_SECRET,
            },
        )

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to get access token from Yandex"
            )

        access_token = token_response.json().get("access_token")

        user_response = await client.get(
            "https://login.yandex.ru/info",
            headers={"Authorization": f"OAuth {access_token}"},
        )

        if user_response.status_code != 200:
            raise HTTPException(
                status_code=400, detail="Failed to get user info from Yandex"
            )

        return user_response.json()
