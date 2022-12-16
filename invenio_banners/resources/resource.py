# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Banners module to create REST APIs."""

from flask import abort, g
from flask_resources import Resource, resource_requestctx, response_handler, route
from invenio_records_resources.resources.records.resource import (
    request_data,
    request_extra_args,
    request_headers,
    request_search_args,
    request_view_args,
)


#
# Resource
#
class BannerResource(Resource):
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
            route("GET", routes["active"], self.read_active),
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

        if banner is None:
            abort(
                404, {"message": "Banner with id {0} is not found.".format(banner_id)}
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

        if banner is None:
            abort(
                404, {"message": "Banner with id {0} is not found.".format(banner_id)}
            )

        return banner.to_dict(), 200

    @request_view_args
    @request_extra_args
    @response_handler()
    def read_active(self):
        """Read active banners."""
        # GET /api/banners?active=true&url_path=url_path
        banners = self.service.read_active(
            identity=g.identity,
            active=resource_requestctx.args.get("active", True),
            url_path=resource_requestctx.args.get("url_path", None),
        )

        return banners.to_dict(), 200

    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over the banners."""
        banners = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
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

        if banner is None:
            abort(
                404, {"message": "Banner with id {0} is not found.".format(banner_id)}
            )

        return banner.to_dict(), 204
