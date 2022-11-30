from fastapi import APIRouter

from core.settings import BASE_URL


def get_auth_route_by_name(routes: list[APIRouter], name: str, base_url: str = BASE_URL):
    for route in routes:
        if route.name == name:
            return BASE_URL + route.path
    raise Exception(f'url with name {name} not found!')
