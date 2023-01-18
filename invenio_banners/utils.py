# -*- coding: utf-8 -*-
#
# Copyright (C) 2020-2023 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""


def style_category(category):
    """Return predefined Semantic-UI classes for each banner category."""
    style_class = "ui {} flashed top attached manage mb-0 message"
    if category == "warning":
        style_class = style_class.format("warning")
    elif category == "other":
        style_class = style_class.format("grey")
    else:
        style_class = style_class.format("info")
    return style_class
