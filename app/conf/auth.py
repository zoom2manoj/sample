#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth

# Auth object creation.
auth = HTTPTokenAuth("Bearer")
