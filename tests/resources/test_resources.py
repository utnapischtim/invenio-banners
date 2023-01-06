# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner resource tests."""
import pytest
from invenio_records_resources.services.errors import PermissionDeniedError


def _create_banner(client, data, headers, status_code=None):
    """Send POST request."""

    result = client.post(
        "/banners/new",
        headers=headers,
        json=data,
    )

    assert result.status_code == status_code
    return result


def test_create_is_forbidden(client, user, request_banner_data, headers):
    """Test that the simple user cannot create a new banner."""

    user.login(client)

    # try to create a banner
    with pytest.raises(PermissionDeniedError):
        _create_banner(client, request_banner_data, headers).json


def test_create_banner(client, admin, request_banner_data, headers):
    """Create a banner."""

    admin.login(client)

    banner = _create_banner(client, request_banner_data, headers, 201).json
    assert banner["message"] == request_banner_data["message"]
    assert banner["url_path"] == request_banner_data["url_path"]
    assert banner["category"] == request_banner_data["category"]
    assert banner["active"] == request_banner_data["active"]
