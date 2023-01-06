# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""API classes for banners in Invenio."""


from invenio_records_resources.records.api import Record

from .models import BannerModel


class Banner(Record):
    """A generic banner record."""

    model_cls = BannerModel
    """The model class for the banner."""
