# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Models."""

from datetime import datetime

from flask import current_app
from invenio_db import db
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy_utils.models import Timestamp

from ..services.errors import BannerNotExistsError


class BannerModel(db.Model, Timestamp):
    """Defines a message to show to users."""

    __tablename__ = "banners"
    __versioned__ = {"versioning": False}

    id = db.Column(db.Integer, primary_key=True)

    message = db.Column(db.Text, nullable=False)
    """The message content."""

    url_path = db.Column(db.String(255), nullable=True)
    """Define in which URL /path the message will be visible."""

    category = db.Column(db.String(20), nullable=False)
    """Category of the message, for styling messages per category."""

    start_datetime = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    """Start date and time (UTC), can be immediate or delayed."""

    end_datetime = db.Column(db.DateTime, nullable=True)
    """End date and time (UTC), must be after `start` or forever if null."""

    active = db.Column(db.Boolean(name="active"), nullable=False, default=True)
    """Defines if the message is active, only one at the same time."""

    @classmethod
    def create(cls, data):
        """Create a new banner."""
        _categories = [t[0] for t in current_app.config["BANNERS_CATEGORIES"]]
        assert data.get("category") in _categories
        with db.session.begin_nested():
            obj = cls(
                message=data.get("message"),
                category=data.get("category"),
                url_path=data.get("url_path"),
                start_datetime=data.get("start_datetime"),
                end_datetime=data.get("end_datetime"),
                active=data.get("active"),
            )
            db.session.add(obj)

        db.session.commit()
        return obj

    @classmethod
    def update(cls, data, id):
        """Update an existing banner."""
        with db.session.begin_nested():
            cls.query.filter_by(id=id).update(data)

        db.session.commit()

    @classmethod
    def get(cls, id):
        """Get banner by its id."""
        try:
            return cls.query.filter_by(id=id).one()
        except NoResultFound:
            raise BannerNotExistsError(id)

    @classmethod
    def delete(cls, banner):
        """Delete banner by its id."""
        with db.session.begin_nested():
            db.session.delete(banner)

        db.session.commit()

    @classmethod
    def get_active(cls, url_path):
        """Return active banners for the given /path."""
        now = datetime.utcnow()

        query = (
            cls.query.filter(cls.active.is_(True))
            .filter(cls.start_datetime <= now)
            .filter((cls.end_datetime.is_(None)) | (now <= cls.end_datetime))
        )

        active_banners = []

        for banner in query.all():
            if banner.url_path is None or url_path.startswith(banner.url_path):
                active_banners.append(banner)

        return active_banners

    @classmethod
    def search(cls, limit, params=None):
        """Filter banners accordingly to query params."""
        query = BannerModel.query

        if params:
            for attr, value in params["facets"].items():
                query = query.filter(getattr(BannerModel, attr) == value[0])

        banners = query.limit(limit).all()
        return banners

    @classmethod
    def disable_expired(cls):
        """Disable any old still active messages to keep everything clean."""
        now = datetime.utcnow()

        query = (
            cls.query.filter(cls.active.is_(True))
            .filter(cls.end_datetime.isnot(None))
            .filter(cls.end_datetime < now)
        )

        for old in query.all():
            old.active = False

        db.session.commit()
