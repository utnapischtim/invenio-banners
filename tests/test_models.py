# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Test models."""

from datetime import datetime, timedelta

import pytest

from invenio_banners.records.models import BannerModel

banners = {
    "everywhere": {
        "message": "everywhere",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "warning": {
        "message": "warning",
        "url_path": None,
        "category": "warning",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "with_end_datetime": {
        "message": "with_end_datetime",
        "url_path": "/",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "end_datetime": datetime.utcnow() + timedelta(days=1),
        "active": True,
    },
    "records_only": {
        "message": "records_only",
        "url_path": "/resources",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "sub_records_only": {
        "message": "sub_records_only",
        "url_path": "/resources/sub",
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
    "disabled": {
        "message": "disabled",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=1),
        "active": False,
    },
    "expired": {
        "message": "expired",
        "url_path": None,
        "category": "info",
        "start_datetime": datetime.utcnow() - timedelta(days=2),
        "end_datetime": datetime.utcnow() - timedelta(days=1),
        "active": True,
    },
}


@pytest.mark.skip(reason="to be fixed")
def test_category(app, db):
    """Test get first active with with path and date."""
    BannerModel.create(**banners["warning"])
    db.session.commit()
    assert BannerModel.get_active().message == "warning"

    with pytest.raises(AssertionError):
        banners["warning"]["category"] = "wrong"
        BannerModel.create(**banners["warning"])


@pytest.mark.skip(reason="to be fixed")
def test_get_with_path_datetime(app, db):
    """Test get first active with with path and date."""
    BannerModel.create(**banners["everywhere"])
    BannerModel.create(**banners["with_end_datetime"])
    BannerModel.create(**banners["disabled"])
    db.session.commit()

    assert BannerModel.get_active("/").message == "everywhere"
    assert BannerModel.get_active("/resources").message == "everywhere"


@pytest.mark.skip(reason="to be fixed")
def test_get_with_specific_path_datetime(app, db):
    """Test get first active with specific path and date."""
    BannerModel.create(**banners["disabled"])
    BannerModel.create(**banners["records_only"])
    db.session.commit()

    assert BannerModel.get_active("/resources").message == "records_only"
    assert BannerModel.get_active("/resources/other").message == "records_only"
    assert BannerModel.get_active("/") is None
    assert BannerModel.get_active("/other") is None


@pytest.mark.skip(reason="to be fixed")
def test_get_with_sub_path_datetime(app, db):
    """Test get first active with sub path and date."""
    BannerModel.create(**banners["disabled"])
    BannerModel.create(**banners["sub_records_only"])
    db.session.commit()

    assert BannerModel.get_active("/resources/sub").message == "sub_records_only"
    assert BannerModel.get_active("/resources") is None
    assert BannerModel.get_active("/") is None
    assert BannerModel.get_active("/other") is None


@pytest.mark.skip(reason="to be fixed")
def test_get_future_datetime(app, db):
    """Test get first active with future date."""
    BannerModel.create(**banners["expired"])
    BannerModel.create(**banners["disabled"])
    BannerModel.create(**banners["records_only"])
    db.session.commit()

    assert BannerModel.get_active("/") is None
    assert BannerModel.get_active("/other") is None
    assert BannerModel.get_active("/resources").message == "records_only"


@pytest.mark.skip(reason="to be fixed")
def test_get_expired_disabled(app, db):
    """Test get first active with future date."""
    BannerModel.create(**banners["expired"])
    BannerModel.create(**banners["disabled"])
    db.session.commit()

    assert BannerModel.get_active("/") is None
    assert BannerModel.get_active("/other") is None
    assert BannerModel.get_active("/resources") is None


@pytest.mark.skip(reason="to be fixed")
def test_disable_expired(app, db):
    """Test clean up old announcement but still active."""
    BannerModel.create(**banners["everywhere"])
    BannerModel.create(**banners["expired"])
    BannerModel.create(**banners["with_end_datetime"])
    BannerModel.create(**banners["sub_records_only"])
    db.session.commit()

    assert BannerModel.query.filter(BannerModel.active.is_(True)).count() == 4

    BannerModel.disable_expired()

    _banners = BannerModel.query.filter(BannerModel.active.is_(True)).all()
    assert len(_banners) == 3
    assert _banners[0].message == "everywhere"
    assert _banners[1].message == "with_end_datetime"
    assert _banners[2].message == "sub_records_only"
