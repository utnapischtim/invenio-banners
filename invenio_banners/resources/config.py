# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banner Resource Configuration."""

from flask_resources import JSONDeserializer, RequestBodyParser
from invenio_records_resources.resources import RecordResourceConfig, \
    SearchRequestArgsSchema


class BannerResourceConfig(RecordResourceConfig):
    """Banner resource config."""

    # Blueprint configuration
    blueprint_name = "banners"
    url_prefix = "/banners"
    routes = {"create": "/new"}

    request_search_args = SearchRequestArgsSchema

    request_body_parsers = {"application/json": RequestBodyParser(JSONDeserializer())}
    default_content_type = "application/json"
