# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Service API."""

from invenio_access.permissions import system_identity
from invenio_records_resources.services import RecordService

from invenio_banners.records.models import BannerModel


class BannerService(RecordService):
    """Banner Service."""

    def read(self, url_path):
        """Retrieve a banner."""
        # TODO: not implemented/tested yet
        # self.require_permission(identity, "read")
        banner = BannerModel.get_active(url_path)
        return self.result_item(self, system_identity, banner)

    def search(self, identity, params=None, **kwargs):
        """Search for resources matching the querystring."""
        # TODO: not implemented/tested yet
        # self.require_permission(identity, "read")
        banners = BannerModel.search()
        return self.result_list(self, system_identity, banners)

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
