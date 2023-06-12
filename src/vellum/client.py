# This file was auto-generated by Fern from our API Definition.

import json
import typing
import urllib.parse
from json.decoder import JSONDecodeError

import httpx
import pydantic

from .core.api_error import ApiError
from .core.jsonable_encoder import jsonable_encoder
from .core.remove_none_from_headers import remove_none_from_headers
from .environment import VellumEnvironment
from .errors.bad_request_error import BadRequestError
from .errors.internal_server_error import InternalServerError
from .errors.not_found_error import NotFoundError
from .resources.deployments.client import AsyncDeploymentsClient, DeploymentsClient
from .resources.document_indexes.client import AsyncDocumentIndexesClient, DocumentIndexesClient
from .resources.documents.client import AsyncDocumentsClient, DocumentsClient
from .resources.model_versions.client import AsyncModelVersionsClient, ModelVersionsClient
from .resources.registered_prompts.client import AsyncRegisteredPromptsClient, RegisteredPromptsClient
from .resources.sandboxes.client import AsyncSandboxesClient, SandboxesClient
from .resources.test_suites.client import AsyncTestSuitesClient, TestSuitesClient
from .types.generate_options_request import GenerateOptionsRequest
from .types.generate_request import GenerateRequest
from .types.generate_response import GenerateResponse
from .types.generate_stream_response import GenerateStreamResponse
from .types.search_request_options_request import SearchRequestOptionsRequest
from .types.search_response import SearchResponse
from .types.submit_completion_actual_request import SubmitCompletionActualRequest

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class Vellum:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key
        self.deployments = DeploymentsClient(environment=self._environment, api_key=self.api_key)
        self.document_indexes = DocumentIndexesClient(environment=self._environment, api_key=self.api_key)
        self.documents = DocumentsClient(environment=self._environment, api_key=self.api_key)
        self.model_versions = ModelVersionsClient(environment=self._environment, api_key=self.api_key)
        self.registered_prompts = RegisteredPromptsClient(environment=self._environment, api_key=self.api_key)
        self.sandboxes = SandboxesClient(environment=self._environment, api_key=self.api_key)
        self.test_suites = TestSuitesClient(environment=self._environment, api_key=self.api_key)

    def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/generate"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def generate_stream(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> typing.Iterator[GenerateStreamResponse]:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        with httpx.stream(
            "POST",
            urllib.parse.urljoin(f"{self._environment.default}/", "v1/generate-stream"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        ) as _response:
            if 200 <= _response.status_code < 300:
                for _text in _response.iter_text():
                    if len(_text) == 0:
                        continue
                    yield pydantic.parse_obj_as(GenerateStreamResponse, json.loads(_text))  # type: ignore
                return
            if _response.status_code == 400:
                raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 404:
                raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            if _response.status_code == 500:
                raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
            try:
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/search"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        _response = httpx.request(
            "POST",
            urllib.parse.urljoin(f"{self._environment.predict}/", "v1/submit-completion-actuals"),
            json=jsonable_encoder(_request),
            headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
            timeout=None,
        )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncVellum:
    def __init__(self, *, environment: VellumEnvironment = VellumEnvironment.PRODUCTION, api_key: str):
        self._environment = environment
        self.api_key = api_key
        self.deployments = AsyncDeploymentsClient(environment=self._environment, api_key=self.api_key)
        self.document_indexes = AsyncDocumentIndexesClient(environment=self._environment, api_key=self.api_key)
        self.documents = AsyncDocumentsClient(environment=self._environment, api_key=self.api_key)
        self.model_versions = AsyncModelVersionsClient(environment=self._environment, api_key=self.api_key)
        self.registered_prompts = AsyncRegisteredPromptsClient(environment=self._environment, api_key=self.api_key)
        self.sandboxes = AsyncSandboxesClient(environment=self._environment, api_key=self.api_key)
        self.test_suites = AsyncTestSuitesClient(environment=self._environment, api_key=self.api_key)

    async def generate(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> GenerateResponse:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/generate"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(GenerateResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def generate_stream(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        requests: typing.List[GenerateRequest],
        options: typing.Optional[GenerateOptionsRequest] = OMIT,
    ) -> typing.AsyncIterator[GenerateStreamResponse]:
        _request: typing.Dict[str, typing.Any] = {"requests": requests}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        if options is not OMIT:
            _request["options"] = options
        async with httpx.AsyncClient() as _client:
            async with _client.stream(
                "POST",
                urllib.parse.urljoin(f"{self._environment.default}/", "v1/generate-stream"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            ) as _response:
                if 200 <= _response.status_code < 300:
                    async for _text in _response.aiter_text():
                        if len(_text) == 0:
                            continue
                        yield pydantic.parse_obj_as(GenerateStreamResponse, json.loads(_text))  # type: ignore
                    return
                if _response.status_code == 400:
                    raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
                if _response.status_code == 404:
                    raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
                if _response.status_code == 500:
                    raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
                try:
                    _response_json = _response.json()
                except JSONDecodeError:
                    raise ApiError(status_code=_response.status_code, body=_response.text)
                raise ApiError(status_code=_response.status_code, body=_response_json)

    async def search(
        self,
        *,
        index_id: typing.Optional[str] = OMIT,
        index_name: typing.Optional[str] = OMIT,
        query: str,
        options: typing.Optional[SearchRequestOptionsRequest] = OMIT,
    ) -> SearchResponse:
        _request: typing.Dict[str, typing.Any] = {"query": query}
        if index_id is not OMIT:
            _request["index_id"] = index_id
        if index_name is not OMIT:
            _request["index_name"] = index_name
        if options is not OMIT:
            _request["options"] = options
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/search"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return pydantic.parse_obj_as(SearchResponse, _response.json())  # type: ignore
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def submit_completion_actuals(
        self,
        *,
        deployment_id: typing.Optional[str] = OMIT,
        deployment_name: typing.Optional[str] = OMIT,
        actuals: typing.List[SubmitCompletionActualRequest],
    ) -> None:
        _request: typing.Dict[str, typing.Any] = {"actuals": actuals}
        if deployment_id is not OMIT:
            _request["deployment_id"] = deployment_id
        if deployment_name is not OMIT:
            _request["deployment_name"] = deployment_name
        async with httpx.AsyncClient() as _client:
            _response = await _client.request(
                "POST",
                urllib.parse.urljoin(f"{self._environment.predict}/", "v1/submit-completion-actuals"),
                json=jsonable_encoder(_request),
                headers=remove_none_from_headers({"X_API_KEY": self.api_key}),
                timeout=None,
            )
        if 200 <= _response.status_code < 300:
            return
        if _response.status_code == 400:
            raise BadRequestError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 404:
            raise NotFoundError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        if _response.status_code == 500:
            raise InternalServerError(pydantic.parse_obj_as(typing.Any, _response.json()))  # type: ignore
        try:
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
