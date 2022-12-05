import aiohttp
from fastapi import APIRouter

from core.settings import BASE_URL


def get_auth_route_by_name(routes: list[APIRouter], name: str, base_url: str = BASE_URL):
    for route in routes:
        if route.name == name:
            return BASE_URL + route.path
    raise Exception(f'url with name {name} not found!')


async def get_http_client() -> aiohttp.ClientSession:
    async with aiohttp.ClientSession() as client:
        yield client
