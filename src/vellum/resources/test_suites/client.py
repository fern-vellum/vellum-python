# This file was auto-generated by Fern from our API Definition.

import typing
from ...core.client_wrapper import SyncClientWrapper
from ...core.request_options import RequestOptions
from ...types.paginated_test_suite_test_case_list import PaginatedTestSuiteTestCaseList
from ...core.jsonable_encoder import jsonable_encoder
from ...core.pydantic_utilities import parse_obj_as
from json.decoder import JSONDecodeError
from ...core.api_error import ApiError
from ...types.named_test_case_variable_value_request import NamedTestCaseVariableValueRequest
from ...types.test_suite_test_case import TestSuiteTestCase
from ...types.test_suite_test_case_bulk_operation_request import TestSuiteTestCaseBulkOperationRequest
from ...types.test_suite_test_case_bulk_result import TestSuiteTestCaseBulkResult
import json
from ...core.client_wrapper import AsyncClientWrapper

# this is used as the default value for optional parameters
OMIT = typing.cast(typing.Any, ...)


class TestSuitesClient:
    def __init__(self, *, client_wrapper: SyncClientWrapper):
        self._client_wrapper = client_wrapper

    def list_test_suite_test_cases(
        self,
        id: str,
        *,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PaginatedTestSuiteTestCaseList:
        """
        List the Test Cases associated with a Test Suite

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        limit : typing.Optional[int]
            Number of results to return per page.

        offset : typing.Optional[int]
            The initial index from which to return the results.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PaginatedTestSuiteTestCaseList


        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suites.list_test_suite_test_cases(
            id="id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            params={
                "limit": limit,
                "offset": offset,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PaginatedTestSuiteTestCaseList,
                    parse_obj_as(
                        type_=PaginatedTestSuiteTestCaseList,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def upsert_test_suite_test_case(
        self,
        id_: str,
        *,
        input_values: typing.Sequence[NamedTestCaseVariableValueRequest],
        evaluation_values: typing.Sequence[NamedTestCaseVariableValueRequest],
        id: typing.Optional[str] = OMIT,
        external_id: typing.Optional[str] = OMIT,
        label: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSuiteTestCase:
        """
        Upserts a new test case for a test suite, keying off of the optionally provided test case id.

        If an id is provided and has a match, the test case will be updated. If no id is provided or no match
        is found, a new test case will be appended to the end.

        Note that a full replacement of the test case is performed, so any fields not provided will be removed
        or overwritten with default values.

        Parameters
        ----------
        id_ : str
            A UUID string identifying this test suite.

        input_values : typing.Sequence[NamedTestCaseVariableValueRequest]
            Values for each of the Test Case's input variables

        evaluation_values : typing.Sequence[NamedTestCaseVariableValueRequest]
            Values for each of the Test Case's evaluation variables

        id : typing.Optional[str]
            The Vellum-generated ID of an existing Test Case whose data you'd like to replace. If specified and no Test Case exists with this ID, a 404 will be returned.

        external_id : typing.Optional[str]
            An ID external to Vellum that uniquely identifies the Test Case that you'd like to create/update. If there's a match on a Test Case that was previously created with the same external_id, it will be updated. Otherwise, a new Test Case will be created with this value as its external_id. If no external_id is specified, then a new Test Case will always be created.

        label : typing.Optional[str]
            A human-readable label used to convey the intention of this Test Case

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteTestCase


        Examples
        --------
        from vellum import NamedTestCaseStringVariableValueRequest, Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suites.upsert_test_suite_test_case(
            id_="id",
            input_values=[
                NamedTestCaseStringVariableValueRequest(
                    name="name",
                )
            ],
            evaluation_values=[
                NamedTestCaseStringVariableValueRequest(
                    name="name",
                )
            ],
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id_)}/test-cases",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "id": id,
                "external_id": external_id,
                "label": label,
                "input_values": input_values,
                "evaluation_values": evaluation_values,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteTestCase,
                    parse_obj_as(
                        type_=TestSuiteTestCase,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    def test_suite_test_cases_bulk(
        self,
        id: str,
        *,
        request: typing.Sequence[TestSuiteTestCaseBulkOperationRequest],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.Iterator[typing.List[TestSuiteTestCaseBulkResult]]:
        """
        Created, replace, and delete Test Cases within the specified Test Suite in bulk

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        request : typing.Sequence[TestSuiteTestCaseBulkOperationRequest]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.Iterator[typing.List[TestSuiteTestCaseBulkResult]]


        Examples
        --------
        from vellum import (
            CreateTestSuiteTestCaseRequest,
            NamedTestCaseStringVariableValueRequest,
            TestSuiteTestCaseCreateBulkOperationRequest,
            Vellum,
        )

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        response = client.test_suites.test_suite_test_cases_bulk(
            id="string",
            request=[
                TestSuiteTestCaseCreateBulkOperationRequest(
                    id="string",
                    data=CreateTestSuiteTestCaseRequest(
                        label="string",
                        input_values=[
                            NamedTestCaseStringVariableValueRequest(
                                value="string",
                                name="string",
                            )
                        ],
                        evaluation_values=[
                            NamedTestCaseStringVariableValueRequest(
                                value="string",
                                name="string",
                            )
                        ],
                        external_id="string",
                    ),
                )
            ],
        )
        for chunk in response:
            yield chunk
        """
        with self._client_wrapper.httpx_client.stream(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases-bulk",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json=request,
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    for _text in _response.iter_lines():
                        try:
                            if len(_text) == 0:
                                continue
                            yield typing.cast(
                                typing.List[TestSuiteTestCaseBulkResult],
                                parse_obj_as(
                                    type_=typing.List[TestSuiteTestCaseBulkResult],  # type: ignore
                                    object_=json.loads(_text),
                                ),
                            )
                        except:
                            pass
                    return
                _response.read()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    def delete_test_suite_test_case(
        self, id: str, test_case_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Deletes an existing test case for a test suite, keying off of the test case id.

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        test_case_id : str
            An id identifying the test case that you'd like to delete

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        from vellum import Vellum

        client = Vellum(
            api_key="YOUR_API_KEY",
        )
        client.test_suites.delete_test_suite_test_case(
            id="id",
            test_case_id="test_case_id",
        )
        """
        _response = self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases/{jsonable_encoder(test_case_id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)


class AsyncTestSuitesClient:
    def __init__(self, *, client_wrapper: AsyncClientWrapper):
        self._client_wrapper = client_wrapper

    async def list_test_suite_test_cases(
        self,
        id: str,
        *,
        limit: typing.Optional[int] = None,
        offset: typing.Optional[int] = None,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> PaginatedTestSuiteTestCaseList:
        """
        List the Test Cases associated with a Test Suite

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        limit : typing.Optional[int]
            Number of results to return per page.

        offset : typing.Optional[int]
            The initial index from which to return the results.

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        PaginatedTestSuiteTestCaseList


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suites.list_test_suite_test_cases(
                id="id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases",
            base_url=self._client_wrapper.get_environment().default,
            method="GET",
            params={
                "limit": limit,
                "offset": offset,
            },
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    PaginatedTestSuiteTestCaseList,
                    parse_obj_as(
                        type_=PaginatedTestSuiteTestCaseList,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def upsert_test_suite_test_case(
        self,
        id_: str,
        *,
        input_values: typing.Sequence[NamedTestCaseVariableValueRequest],
        evaluation_values: typing.Sequence[NamedTestCaseVariableValueRequest],
        id: typing.Optional[str] = OMIT,
        external_id: typing.Optional[str] = OMIT,
        label: typing.Optional[str] = OMIT,
        request_options: typing.Optional[RequestOptions] = None,
    ) -> TestSuiteTestCase:
        """
        Upserts a new test case for a test suite, keying off of the optionally provided test case id.

        If an id is provided and has a match, the test case will be updated. If no id is provided or no match
        is found, a new test case will be appended to the end.

        Note that a full replacement of the test case is performed, so any fields not provided will be removed
        or overwritten with default values.

        Parameters
        ----------
        id_ : str
            A UUID string identifying this test suite.

        input_values : typing.Sequence[NamedTestCaseVariableValueRequest]
            Values for each of the Test Case's input variables

        evaluation_values : typing.Sequence[NamedTestCaseVariableValueRequest]
            Values for each of the Test Case's evaluation variables

        id : typing.Optional[str]
            The Vellum-generated ID of an existing Test Case whose data you'd like to replace. If specified and no Test Case exists with this ID, a 404 will be returned.

        external_id : typing.Optional[str]
            An ID external to Vellum that uniquely identifies the Test Case that you'd like to create/update. If there's a match on a Test Case that was previously created with the same external_id, it will be updated. Otherwise, a new Test Case will be created with this value as its external_id. If no external_id is specified, then a new Test Case will always be created.

        label : typing.Optional[str]
            A human-readable label used to convey the intention of this Test Case

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        TestSuiteTestCase


        Examples
        --------
        import asyncio

        from vellum import AsyncVellum, NamedTestCaseStringVariableValueRequest

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suites.upsert_test_suite_test_case(
                id_="id",
                input_values=[
                    NamedTestCaseStringVariableValueRequest(
                        name="name",
                    )
                ],
                evaluation_values=[
                    NamedTestCaseStringVariableValueRequest(
                        name="name",
                    )
                ],
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id_)}/test-cases",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json={
                "id": id,
                "external_id": external_id,
                "label": label,
                "input_values": input_values,
                "evaluation_values": evaluation_values,
            },
            request_options=request_options,
            omit=OMIT,
        )
        try:
            if 200 <= _response.status_code < 300:
                return typing.cast(
                    TestSuiteTestCase,
                    parse_obj_as(
                        type_=TestSuiteTestCase,  # type: ignore
                        object_=_response.json(),
                    ),
                )
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)

    async def test_suite_test_cases_bulk(
        self,
        id: str,
        *,
        request: typing.Sequence[TestSuiteTestCaseBulkOperationRequest],
        request_options: typing.Optional[RequestOptions] = None,
    ) -> typing.AsyncIterator[typing.List[TestSuiteTestCaseBulkResult]]:
        """
        Created, replace, and delete Test Cases within the specified Test Suite in bulk

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        request : typing.Sequence[TestSuiteTestCaseBulkOperationRequest]

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Yields
        ------
        typing.AsyncIterator[typing.List[TestSuiteTestCaseBulkResult]]


        Examples
        --------
        import asyncio

        from vellum import (
            AsyncVellum,
            CreateTestSuiteTestCaseRequest,
            NamedTestCaseStringVariableValueRequest,
            TestSuiteTestCaseCreateBulkOperationRequest,
        )

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            response = await client.test_suites.test_suite_test_cases_bulk(
                id="string",
                request=[
                    TestSuiteTestCaseCreateBulkOperationRequest(
                        id="string",
                        data=CreateTestSuiteTestCaseRequest(
                            label="string",
                            input_values=[
                                NamedTestCaseStringVariableValueRequest(
                                    value="string",
                                    name="string",
                                )
                            ],
                            evaluation_values=[
                                NamedTestCaseStringVariableValueRequest(
                                    value="string",
                                    name="string",
                                )
                            ],
                            external_id="string",
                        ),
                    )
                ],
            )
            async for chunk in response:
                yield chunk


        asyncio.run(main())
        """
        async with self._client_wrapper.httpx_client.stream(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases-bulk",
            base_url=self._client_wrapper.get_environment().default,
            method="POST",
            json=request,
            request_options=request_options,
            omit=OMIT,
        ) as _response:
            try:
                if 200 <= _response.status_code < 300:
                    async for _text in _response.aiter_lines():
                        try:
                            if len(_text) == 0:
                                continue
                            yield typing.cast(
                                typing.List[TestSuiteTestCaseBulkResult],
                                parse_obj_as(
                                    type_=typing.List[TestSuiteTestCaseBulkResult],  # type: ignore
                                    object_=json.loads(_text),
                                ),
                            )
                        except:
                            pass
                    return
                await _response.aread()
                _response_json = _response.json()
            except JSONDecodeError:
                raise ApiError(status_code=_response.status_code, body=_response.text)
            raise ApiError(status_code=_response.status_code, body=_response_json)

    async def delete_test_suite_test_case(
        self, id: str, test_case_id: str, *, request_options: typing.Optional[RequestOptions] = None
    ) -> None:
        """
        Deletes an existing test case for a test suite, keying off of the test case id.

        Parameters
        ----------
        id : str
            A UUID string identifying this test suite.

        test_case_id : str
            An id identifying the test case that you'd like to delete

        request_options : typing.Optional[RequestOptions]
            Request-specific configuration.

        Returns
        -------
        None

        Examples
        --------
        import asyncio

        from vellum import AsyncVellum

        client = AsyncVellum(
            api_key="YOUR_API_KEY",
        )


        async def main() -> None:
            await client.test_suites.delete_test_suite_test_case(
                id="id",
                test_case_id="test_case_id",
            )


        asyncio.run(main())
        """
        _response = await self._client_wrapper.httpx_client.request(
            f"v1/test-suites/{jsonable_encoder(id)}/test-cases/{jsonable_encoder(test_case_id)}",
            base_url=self._client_wrapper.get_environment().default,
            method="DELETE",
            request_options=request_options,
        )
        try:
            if 200 <= _response.status_code < 300:
                return
            _response_json = _response.json()
        except JSONDecodeError:
            raise ApiError(status_code=_response.status_code, body=_response.text)
        raise ApiError(status_code=_response.status_code, body=_response_json)
