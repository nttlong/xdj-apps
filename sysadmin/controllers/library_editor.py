#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Controller này dùng để quản lý mục librabry
"""
import xdj
@xdj.Controller(
    url="library/library",
    template="library/library.html"
)
class library_controller(xdj.BaseController):
    pass