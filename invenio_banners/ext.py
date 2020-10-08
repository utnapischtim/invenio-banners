# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio extension app."""

from . import config


class InvenioBanners(object):
    """Invenio-Banners extension."""

    def __init__(self, app=None):
        """Extension initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        app.extensions["invenio-banners"] = self

    def init_config(self, app):
        """Initialize configuration."""
        # Use theme's base template if theme is installed
        if "BASE_TEMPLATE" in app.config:
            app.config.setdefault(
                "BANNERS_BASE_TEMPLATE", app.config["BASE_TEMPLATE"]
            )
        for k in dir(config):
            if k.startswith("BANNERS_"):
                app.config.setdefault(k, getattr(config, k))
