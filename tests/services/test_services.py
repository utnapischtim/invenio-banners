# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service level tests for Banners."""

import pytest
from invenio_records_resources.services.errors import PermissionDeniedError

from invenio_banners.proxies import current_banners_service


def test_banner_creation(app, superuser_identity, request_banner_data):
    service = current_banners_service

    banner = service.create(superuser_identity, request_banner_data)
    banner = banner.to_dict()

    assert banner["message"] == "Banner message"
    assert banner["url_path"] == "/url_path"
    assert banner["category"] == "warning"
    assert banner["active"] is True


def test_create_is_forbidden(app, simple_user_identity, request_banner_data):
    """Test that the simple user cannot create a new banner."""

    service = current_banners_service

    with pytest.raises(PermissionDeniedError):
        service.create(simple_user_identity, request_banner_data)
