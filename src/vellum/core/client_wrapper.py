# This file was auto-generated by Fern from our API Definition.

import typing

import httpx

from ..environment import VellumEnvironment


class BaseClientWrapper:
    def __init__(self, *, api_key: str, environment: VellumEnvironment):
        self.api_key = api_key
        self._environment = environment

    def get_headers(self) -> typing.Dict[str, str]:
        headers: typing.Dict[str, str] = {
            "X-Fern-Language": "Python",
            "X-Fern-SDK-Name": "vellum-ai",
            "X-Fern-SDK-Version": "v0.1.5",
        }
        headers["X_API_KEY"] = self.api_key
        return headers

    def get_environment(self) -> VellumEnvironment:
        return self._environment


class SyncClientWrapper(BaseClientWrapper):
    def __init__(self, *, api_key: str, environment: VellumEnvironment, httpx_client: httpx.Client):
        super().__init__(api_key=api_key, environment=environment)
        self.httpx_client = httpx_client


class AsyncClientWrapper(BaseClientWrapper):
    def __init__(self, *, api_key: str, environment: VellumEnvironment, httpx_client: httpx.AsyncClient):
        super().__init__(api_key=api_key, environment=environment)
        self.httpx_client = httpx_client
