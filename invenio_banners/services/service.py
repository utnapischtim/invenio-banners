# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Service API."""

from invenio_records_resources.services import RecordService
from invenio_records_resources.services.base import LinksTemplate

from ..records.models import BannerModel
from ..services.errors import BannerNotExistsError


class BannerService(RecordService):
    """Banner Service."""

    def read(self, identity, id):
        """Retrieve a banner."""
        # resolve and require permission
        self.require_permission(identity, "read")

        banner = self.record_cls.get(id)

        # check if banner exists
        if banner is None:
            raise BannerNotExistsError(id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )

    def read_active(self, identity, active, url_path, params=None):
        """Retrieve a banner."""
        # resolve and require permission
        self.require_permission(identity, "read")

        banners = self.record_cls.get_active(active, url_path)

        return self.result_list(
            self,
            identity,
            banners,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def search(self, identity, params=None):
        """Search for banners matching the querystring."""
        self.require_permission(identity, "search")

        banners = BannerModel.query.all()
        return self.result_list(
            self,
            identity,
            banners,
            links_tpl=LinksTemplate(self.config.links_search, context={"args": params}),
            links_item_tpl=self.links_item_tpl,
        )

    def create(self, identity, data, raise_errors=True):
        """Create a banner."""
        self.require_permission(identity, "create")

        # validate data
        data, errors = self.schema.load(
            data,
            context={"identity": identity},
            raise_errors=False,
        )

        # create the banner with the specified data
        banner = self.record_cls.create(data)

        return self.result_item(
            self, identity, banner, links_tpl=self.links_item_tpl, errors=errors
        )

    def delete(self, identity, id):
        """Delete a banner from database."""
        self.require_permission(identity, "delete")

        # check if banner exists
        banner = self.record_cls.get(id)
        if banner is None:
            raise BannerNotExistsError(id)

        self.record_cls.delete(banner)

        return self.result_item(self, identity, banner, links_tpl=self.links_item_tpl)

    def update(self, identity, id, data):
        """Update a banner."""
        self.require_permission(identity, "update")

        # check if banner exists
        banner = self.record_cls.get(id)
        if banner is None:
            raise BannerNotExistsError(id)

        self.record_cls.update(data, id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )
