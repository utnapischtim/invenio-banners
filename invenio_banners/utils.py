# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Utils."""


def style_category(category):
    """Return predefined Boostrap CSS classes for each banner category."""
    css_class = "alert alert-{}"
    if category == "warning":
        css_class = css_class.format("warning")
    elif category == "other":
        css_class = css_class.format("secondary")
    else:
        css_class = css_class.format("primary")
    return css_class
