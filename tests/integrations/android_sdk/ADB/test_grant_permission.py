import subprocess
from unittest.mock import MagicMock

import pytest

from briefcase.exceptions import BriefcaseCommandError


@pytest.mark.parametrize(
    "permission",
    ["android.permission.READ_CALENDAR", "com.example.permission.CUSTOM"],
)
def test_grant_permission(adb, capsys, permission):
    """Grant the exact permission name without displaying subprocess output."""
    adb.run = MagicMock(return_value="normal adb output")

    adb.grant_permission("com.example.sample.package", permission)

    adb.run.assert_called_once_with(
        "shell",
        "pm",
        "grant",
        "com.example.sample.package",
        permission,
    )
    assert "normal adb output" not in capsys.readouterr().out


def test_grant_permission_failure(adb):
    """Failed grants report the permission, package, and selected device."""
    failure = subprocess.CalledProcessError(returncode=1, cmd="pm grant")
    adb.run = MagicMock(side_effect=failure)

    with pytest.raises(
        BriefcaseCommandError,
        match=(
            "Unable to grant permission android.permission.READ_CALENDAR "
            f"for app com.example.sample.package on {adb.device}"
        ),
    ) as exc_info:
        adb.grant_permission(
            "com.example.sample.package",
            "android.permission.READ_CALENDAR",
        )

    assert exc_info.value.__cause__ is failure
    adb.run.assert_called_once_with(
        "shell",
        "pm",
        "grant",
        "com.example.sample.package",
        "android.permission.READ_CALENDAR",
    )
