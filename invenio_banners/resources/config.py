# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Resource Configuration."""

import marshmallow as ma
from flask_resources import JSONDeserializer, RequestBodyParser
from invenio_records_resources.resources import RecordResourceConfig, \
    SearchRequestArgsSchema


class BannerResourceConfig(RecordResourceConfig):
    """Banner resource config."""

    # Blueprint configuration
    blueprint_name = "banners"
    url_prefix = "/banners"
    routes = {
        "create": "/new",
        "item": "/<banner_id>",
        "list": "/",
    }

    request_view_args = {
        "banner_id": ma.fields.String(),
    }

    request_extra_args = {
        "active": ma.fields.Boolean(),
        "url_path": ma.fields.String(),
    }

    request_search_args = SearchRequestArgsSchema

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}
    default_content_type = "application/json"
