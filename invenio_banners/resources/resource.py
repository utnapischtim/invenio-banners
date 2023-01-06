# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Invenio Banners module to create REST APIs."""

from flask import g
from flask_resources import Resource, resource_requestctx, response_handler, \
    route
from invenio_records_resources.resources.records.resource import \
    request_data, request_search_args, request_view_args


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
        ]

    #
    # Primary Interface
    #
    @request_view_args
    @response_handler()
    def read(self):
        """Read an item."""
        # TODO: not implemented/tested yet

        item = self.service.read(url_path=resource_requestctx.view_args["url_path"])
        return item.to_dict(), 200

    @request_search_args
    @request_view_args
    @response_handler(many=True)
    def search(self):
        """Perform a search over banners."""
        # TODO: not implemented/tested yet

        banners = self.service.search(
            identity=g.identity,
            params=resource_requestctx.args,
        )

        return banners, 200

    @request_data
    @response_handler()
    def create(self):
        """Create a banner."""
        item = self.service.create(
            g.identity,
            resource_requestctx.data or {},
        )

        return item.to_dict(), 201
