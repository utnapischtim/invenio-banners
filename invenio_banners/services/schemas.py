# -*- coding: utf-8 -*-
#
# Copyright (C) 2022-2023 CERN.
# Copyright (C) 2024 Graz University of Technology.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Banners schema."""

from datetime import timezone

from invenio_db import now
from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import fields, pre_load
from marshmallow_utils.fields import TZDateTime


class BannerSchema(BaseRecordSchema):
    """Schema for banners."""

    message = fields.String(required=True)
    url_path = fields.String(allow_none=True)
    category = fields.String(required=True, metadata={"default": "info"})
    start_datetime = fields.DateTime(
        required=True,
        metadata={"default": now().strftime("%Y-%m-%d %H:%M:%S")},
    )
    end_datetime = fields.DateTime(allow_none=True)
    active = fields.Boolean(required=True, metadata={"default": True})
    created = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)
    updated = TZDateTime(timezone=timezone.utc, format="iso", dump_only=True)

    @pre_load
    def change_none_to_string(self, data, **kwargs):
        """Fix for empty strings not in line with allow_none=True."""
        for field in data:
            if field == "end_datetime" or field == "category":
                if data[field] == "":
                    data[field] = None
        return data
