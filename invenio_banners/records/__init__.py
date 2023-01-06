# -*- coding: utf-8 -*-
#
# Copyright (C) 2022 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Records directory."""


from .api import Banner
from .models import BannerModel

__all__ = (
    "Banner",
    "BannerModel",
)
