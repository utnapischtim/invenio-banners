# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Service results."""
from invenio_records_resources.services.records.results import RecordItem, \
    RecordList


class BannerItem(RecordItem):
    """Single banner result."""

    def __init__(
        self,
        service,
        identity,
        banner,
        links_tpl=None,
        errors=None,
        schema=None,
    ):
        """Constructor."""
        self._banner = banner
        self._identity = identity
        self._service = service
        self._data = None
        self._schema = schema or service.schema
        self._links_tpl = links_tpl
        self._errors = errors
        super().__init__(service, identity, banner)

    @property
    def _obj(self):
        """Return the object to dump."""
        return self._banner

    @property
    def links(self):
        """Get links for this result item."""
        return self._links_tpl.expand(self._identity, self._banner)

    @property
    def data(self):
        """Property to get the banner."""
        if self._data:
            return self._data

        self._data = self._schema.dump(
            self._obj,
            context={
                "identity": self._identity,
                "record": self._banner,
            },
        )

        if self._links_tpl:
            self._data["links"] = self.links

        return self._data


class BannerList(RecordList):
    """List of banner results."""

    # TODO: not implemented/tested yet

    def __init__(
        self,
        service,
        identity,
        banners,
        params=None,
        links_tpl=None,
        links_item_tpl=None,
    ):
        """Constructor.

        :params service: a service instance
        :params identity: an identity that performed the service request
        :params banners: the search results
        :params params: dictionary of the query parameters
        """
        self._identity = identity
        self._results = banners
        self._service = service
        self._params = params
        self._links_tpl = links_tpl
        self._links_item_tpl = links_item_tpl
        super().__init__(service, identity, banners)

    @property
    def results(self):
        """Get links for this result item."""
        return self._results
