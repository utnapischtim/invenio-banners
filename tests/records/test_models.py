# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test models."""

from datetime import datetime, timedelta

import pytest

from invenio_banners.records.models import BannerModel
from invenio_banners.services.errors import BannerNotExistsError

banners = {
    "valid": {
        "message": "valid",
        "url_path": "/valid",
        "category": "info",
        "end_datetime": datetime.utcnow() + timedelta(days=1),
        "active": True,
    },
    "everywhere": {
        "message": "everywhere",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "with_end_datetime": {
        "message": "with_end_datetime",
        "url_path": "/with_end_datetime",
        "category": "info",
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "sub_records_only": {
        "message": "sub_records_only",
        "url_path": "/resources/sub",
        "category": "warning",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "disabled": {
        "message": "disabled",
        "url_path": "/disabled",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": False,
    },
    "expired": {
        "message": "expired",
        "url_path": "/expired",
        "category": "warning",
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
}


def test_get_active_with_datetime(app):
    """Test get active with end_datetime in past."""
    BannerModel.create(banners["with_end_datetime"])
    assert BannerModel.get_active() == []


def test_get_active_future_datetime(app, db):
    """Test get active with future date."""
    BannerModel.create(banners["expired"])
    assert BannerModel.get_active() == []


def test_get_active_disabled(app, db):
    """Test get non-active."""
    BannerModel.create(banners["disabled"])
    assert BannerModel.get_active() == []


def test_get_active(app):
    """Test get active banner."""
    # create banners first
    BannerModel.create(banners["sub_records_only"])
    BannerModel.create(banners["disabled"])

    assert len(BannerModel.get_active()) == 1
    assert BannerModel.get_active()[0].message == "sub_records_only"


def test_create_banner(app):
    """Create a banner."""
    banner = BannerModel.create(banners["valid"])

    db_banner = BannerModel.query.filter_by(id=banner.id).one()
    assert db_banner.message == banner.message
    assert db_banner.category == banner.category
    assert db_banner.url_path == banner.url_path
    assert db_banner.active == banner.active


def test_update_banner(app):
    """Update a banner."""
    # create banner first
    banner = BannerModel.create(banners["valid"])

    new_data = {
        "message": "New banner message",
        "category": "other",
    }

    BannerModel.update(new_data, banner.id)

    db_banner = BannerModel.query.filter_by(id=banner.id).one()
    assert db_banner.message == new_data["message"]
    assert db_banner.category == new_data["category"]
    assert db_banner.url_path == banner.url_path
    assert db_banner.active == banner.active


def test_delete_banner(app):
    """Delete a banner."""
    # create banner first
    banner = BannerModel.create(banners["valid"])

    BannerModel.delete(banner)

    # check that it's not present in db
    assert BannerModel.query.filter_by(id=banner.id).one_or_none() is None


def test_get_banner(app):
    """Get a banner by id."""
    # create banner first
    banner = BannerModel.create(banners["valid"])

    banner_result = BannerModel.get(banner.id)
    assert banner_result.message == banner.message
    assert banner_result.category == banner.category
    assert banner_result.url_path == banner.url_path
    assert banner_result.active == banner.active


def test_get_non_existing_banner(app):
    """Get a non-existing banner."""
    # create banner first
    with pytest.raises(BannerNotExistsError) as ex:
        BannerModel.get("000")

    assert ex.value.description == "Banner with id 000 is not found."


def test_category(app):
    """Test create banner with incorrect category."""
    banner = BannerModel.get(1)
    assert banner.message == "with_end_datetime"
    assert banner.category == "info"

    with pytest.raises(AssertionError):
        banners["with_end_datetime"]["category"] = "wrong"
        BannerModel.create(banners["with_end_datetime"])
