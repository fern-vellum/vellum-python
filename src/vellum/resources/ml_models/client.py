# This file was auto-generated by Fern from our API Definition.

from ...core.client_wrapper import SyncClientWrapper
import typing
from ...core.request_options import RequestOptions
from ...types.ml_model_read import MlModelRead
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...core.client_wrapper import AsyncClientWrapper


class MlModelsClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def retrieve(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> MlModelRead:
        """
        Retrieve details about an ML Model

        Parameters
        ----------
        id : str
            Either the ML Model's ID, its unique name, or its ID in the workspace.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        MlModelRead


        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.ml_models.retrieve(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/ml-models/{jsonable_encoder(id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    MlModelRead,
                    parse_obj_as(
                        type_=MlModelRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncMlModelsClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def retrieve(self, id: str, *, request_options: typing.Optional[RequestOptions] = None) -> MlModelRead:
        """
        Retrieve details about an ML Model

        Parameters
        ----------
        id : str
            Either the ML Model's ID, its unique name, or its ID in the workspace.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        MlModelRead


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.ml_models.retrieve(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/ml-models/{jsonable_encoder(id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    MlModelRead,
                    parse_obj_as(
                        type_=MlModelRead,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
