# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio extension app."""

from invenio_banners.services import BannerService, BannerServiceConfig

from . import config
from .resources import BannerResource, BannerResourceConfig
from .services import BannerService, BannerServiceConfig


class InvenioBanners(object):
    """Invenio-Banners extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_services(app)
        self.init_resources(app)
        app.extensions["invenio-banners"] = self

    def init_config(self, app):
        """Initialize configuration."""
        for k in dir(config):
            if k.startswith("BANNERS_"):
                app.config.setdefault(k, getattr(config, k))

    def init_services(self, app):
        """Initialize the services for banners."""
        self.banners_service = BannerService(config=BannerServiceConfig)

    def init_resources(self, app):
        """Initialize the resources for banners."""
        self.banners_resource = BannerResource(
            service=self.banners_service,
            config=BannerResourceConfig,
        )
