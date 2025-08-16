import httpx

async def fetch_json(url: str, params: dict, timeout: float = 30.0) -> dict:
    """
    Асинхронный GET-запрос, возвращает JSON.
    Обрабатывает ошибки и тайм-ауты.
    """
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        print(f"Ошибка запроса: {e}")
    except httpx.TimeoutException:
        print(f"Тайм-аут запроса к {url}")
    return {}