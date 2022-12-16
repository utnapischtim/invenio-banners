# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banners Service configuration."""

from invenio_records_resources.services import Link, RecordServiceConfig
from invenio_records_resources.services.records.links import pagination_links

from ..records.models import BannerModel
from .permissions import BannersPermissionPolicy
from .results import BannerItem, BannerList
from .schemas import BannerSchema


class BannersLink(Link):
    """Link variables setter for Banner links."""

    @staticmethod
    def vars(banner, vars):
        """Variables for the URI template."""
        vars.update({"id": banner.id})


class BannerServiceConfig(RecordServiceConfig):
    """Service factory configuration."""

    result_item_cls = BannerItem
    result_list_cls = BannerList
    permission_policy_cls = BannersPermissionPolicy
    schema = BannerSchema

    # links configuration
    links_item = {
        "self": BannersLink("{+api}/banners/{id}"),
    }
    links_search = pagination_links("{+api}/banners{?args*}")
    record_cls = BannerModel
