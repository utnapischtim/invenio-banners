# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Banners module to create REST APIs."""

from flask import g
from flask_resources import Resource, resource_requestctx, response_handler, route
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
    request_headers,
    request_search_args,
    request_view_args,
)

from .errors import ErrorHandlersMixin

from .errors import ErrorHandlersMixin


#
# Resource
#
class BannerResource(ErrorHandlersMixin, Resource):
    """Banner resource."""

    def __init__(self, config, service):
        """Constructor."""
        super(BannerResource, self).__init__(config)
        self.service = service

    def create_url_rules(self):
        """Create the URL rules for the record resource."""
        routes = self.config.routes
        return [
            route("POST", routes["create"], self.create),
            route("GET", routes["banner"], self.read),
            route("GET", routes["list"], self.search),
            route("DELETE", routes["banner"], self.delete),
            route("PUT", routes["banner"], self.update),
        ]

    @request_view_args
    @request_data
    @response_handler()
    def update(self):
        """Update a banner."""
        banner_id = resource_requestctx.view_args["banner_id"]
        banner = self.service.update(
            id=banner_id,
            identity=g.identity,
            data=resource_requestctx.data,
        )

        return banner.to_dict(), 200

    @request_view_args
    @response_handler()
    def read(self):
        """Read a banner."""
        banner_id = resource_requestctx.view_args["banner_id"]
        banner = self.service.read(
            id=banner_id,
            identity=g.identity,
        )

        return banner.to_dict(), 200

    @request_search_args
    @request_view_args
    @request_extra_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the banners."""
        active_arg = resource_requestctx.args.get("active")

        if active_arg is None:
            # Search for all the records:
            # GET /api/banners
            banners = self.service.search(
                identity=g.identity,
            )
        else:
            # Search for records filtered by 'active' and 'url_path' fields:
            # GET /api/banners?active=true&url_path=url_path
            banners = self.service.read_active(
                identity=g.identity,
                active=active_arg,
                url_path=resource_requestctx.args.get("url_path", None),
            )

        return banners.to_dict(), 200

    @request_data
    @response_handler()
    def create(self):
        """Create a banner."""
        banner = self.service.create(
            g.identity,
            resource_requestctx.data or {},
        )

        return banner.to_dict(), 201

    @request_headers
    @request_view_args
    def delete(self):
        """Delete a banner."""
        banner_id = resource_requestctx.view_args["banner_id"]
        banner = self.service.delete(
            id=banner_id,
            identity=g.identity,
        )

        return banner.to_dict(), 204
