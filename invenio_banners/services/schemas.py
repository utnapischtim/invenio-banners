# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banners schema."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import fields


class BannerSchema(BaseRecordSchema):
    """Schema for banners."""

    message = fields.String()
    url_path = fields.String()
    category = fields.String()
    start_datetime = fields.DateTime()
    end_datetime = fields.DateTime()
    active = fields.Boolean()
