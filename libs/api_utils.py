# coding: utf-8
#
# Copyright (C) 2020, Team Kodi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Functions to interact with various web site APIs"""

from __future__ import absolute_import, unicode_literals

import json
from urllib2 import Request, urlopen
from urllib2 import URLError
from urllib import urlencode
from pprint import pformat
from .utils import logger
try:
    from typing import Text, Optional, Union, List, Dict, Any  # pylint: disable=unused-import
    InfoType = Dict[Text, Any]  # pylint: disable=invalid-name
except ImportError:
    pass

HEADERS = {}


def set_headers(headers):
    HEADERS.update(headers)


def load_info(url, params=None, default=None, resp_type='json', verboselog=False):
    if params:
        url = url + '?' + urllib.urlencode(params)  # 使用 urllib 的 urlencode
    logger.debug('Calling URL "{}"'.format(url))
    req = urllib2.Request(url, headers=HEADERS)
    try:
        response = urllib2.urlopen(req, timeout=10)  # 设置超时为 1 秒
    except urllib2.URLError as e:
        if hasattr(e, 'reason'):
            logger.debug('Failed to reach the remote site\nReason: {}'.format(e.reason))
        elif hasattr(e, 'code'):
            logger.debug('Remote site unable to fulfill the request\nError code: {}'.format(e.code))
        return default  # 直接返回默认值

    if response is None:
        return default

    # 检查 Content-Type 以确定编码
    content_type = response.headers.get('Content-Type', '')
    encoding = 'utf-8'  # 默认编码
    if 'charset=' in content_type:
        encoding = content_type.split('charset=')[-1]

    if resp_type.lower() == 'json':
        try:
            resp = json.loads(response.read().decode(encoding))
        except ValueError as e:
            logger.debug('JSON decode error: {}'.format(e))
            return default
    else:
        resp = response.read().decode(encoding)

    if verboselog:
        logger.debug('The API response:\n{}'.format(pprint.pformat(resp)))  # 使用 pprint.pformat 进行格式化

    return resp


