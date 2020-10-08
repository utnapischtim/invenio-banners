# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 CERN.
#
# Invenio-Banners is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Views."""

from flask import Blueprint

blueprint = Blueprint("invenio_banners", __name__)


@blueprint.route("/banners")
def banners():
    """Return the list of banners."""
    pass
