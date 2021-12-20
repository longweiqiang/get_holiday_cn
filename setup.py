#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/11 1:38 下午
# @Author  : Weiqiang.long
# @Email    : 573925242@qq.com
# @File    : setup.py
# @Software: PyCharm

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "get_holiday_cn",
    version = "1.0.3",
    author = "Weiqiang.long",
    description = "获取中国法定节假日",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url = "https://github.com/longweiqiang/get_holiday_cn",
    packages = setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]

)