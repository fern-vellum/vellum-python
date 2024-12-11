import pytest
from datetime import datetime
import glob
import os
from typing import List, Optional, Set, Tuple

from vellum import WorkspaceSecretRead

current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(os.path.abspath(__file__))
all_fixtures = glob.glob(os.path.join(current_dir, "fixtures/**"))


def _get_fixtures(
    exclude_fixtures: Optional[Set[str]] = None, include_fixtures: Optional[Set[str]] = None
) -> List[str]:
    return [
        f
        for f in all_fixtures
        if (exclude_fixtures is None or os.path.basename(f) not in exclude_fixtures)
        and (include_fixtures is None or os.path.basename(f) in include_fixtures)
    ]


def _get_fixture_paths(root: str) -> Tuple[str, str]:
    display_file = os.path.join(root, "display_data", f"{root.split('/')[-1]}.json")
    code_dir = os.path.join(root, "code")

    return display_file, code_dir


_fixture_paths = _get_fixtures(
    # TODO: Remove exclusions on all of these fixtures
    # https://app.shortcut.com/vellum/story/4649/remove-fixture-exclusions-for-serialization
    exclude_fixtures={
        "simple_merge_node",
        "faa_q_and_a_bot",
        # TODO: Remove the bottom three in fast follows
        "simple_inline_subworkflow_node",
        "simple_map_node",
    }
)
_fixture_ids = [os.path.basename(path) for path in _fixture_paths]


@pytest.fixture(
    params=_fixture_paths,
    ids=_fixture_ids,
)
def code_to_display_fixture_paths(request) -> Tuple[str, str]:
    root = request.param
    return _get_fixture_paths(root)


@pytest.fixture
def workspace_secret_client(vellum_client):
    workspace_secret = WorkspaceSecretRead(
        id="cecd16a2-4de5-444d-acff-37a5c400600c",
        modified=datetime.now(),
        name="MY_SECRET",
        label="My Secret",
        secret_type="USER_DEFINED",
    )
    vellum_client.workspace_secrets.retrieve.return_value = workspace_secret
