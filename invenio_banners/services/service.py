# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Service API."""

from invenio_records_resources.services import RecordService
from invenio_records_resources.services.base import LinksTemplate


class BannerService(RecordService):
    """Banner Service."""

    def read(self, identity, id):
        """Retrieve a banner."""
        self.require_permission(identity, "read")

        banner = self.record_cls.get(id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )

    def read_active_banners(self, identity, url_path):
        """Retrieve the list of active banners with the given url_path."""
        self.require_permission(identity, "read")

        banners = self.record_cls.get_active(url_path)

        return self.result_list(
            self,
            identity,
            banners,
            links_item_tpl=self.links_item_tpl,
        )

    def search(self, identity, limit=100, params=None):
        """Search for banners matching the querystring."""
        self.require_permission(identity, "search")

        banners = self.record_cls.search(limit, params)

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

        banner = self.record_cls.get(id)

        self.record_cls.delete(banner)

        return self.result_item(self, identity, banner, links_tpl=self.links_item_tpl)

    def update(self, identity, id, data):
        """Update a banner."""
        self.require_permission(identity, "update")

        banner = self.record_cls.get(id)

        self.record_cls.update(data, id)

        return self.result_item(
            self,
            identity,
            banner,
            links_tpl=self.links_item_tpl,
        )

    def disable_expired(self, identity):
        """Disable expired banners."""
        self.require_permission(identity, "disable")
        self.record_cls.disable_expired()
