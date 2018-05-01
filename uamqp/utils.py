#-------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#--------------------------------------------------------------------------

import uuid
from datetime import timedelta
import time
import base64

from uamqp import types
from uamqp import c_uamqp


def parse_connection_string(connect_str):
    connect_info = {}
    fields = connect_str.split(';')
    for field in fields:
        key, value = field.split('=', 1)
        connect_info[key] = value
    return connect_info


def create_sas_token(key_name, shared_access_key, scope, expiry=timedelta(hours=1)):
    shared_access_key = base64.b64encode(shared_access_key)
    abs_expiry = int(time.time()) + expiry.seconds
    return c_uamqp.create_sas_token(shared_access_key, scope, key_name, abs_expiry)


def data_factory(value):
    result = None
    if value is None:
        result = c_uamqp.null_value()
    elif isinstance(value, types.AMQPType):
        result = value.c_data
    elif isinstance(value, c_uamqp.AMQPValue):
        result = value
    elif isinstance(value, bool):
        result = c_uamqp.bool_value(value)
    elif isinstance(value, str) and len(value) == 1:
        result = c_uamqp.char_value(value.encode('utf-8'))
    elif isinstance(value, str) and len(value) > 1:
        result = c_uamqp.string_value(value.encode('utf-8'))
    elif isinstance(value, uuid.UUID):
        result = c_uamqp.uuid_value(value)
    elif isinstance(value, bytes):
        result = c_uamqp.binary_value(value)
    elif isinstance(value, float):
        result = c_uamqp.double_value(value)
    elif isinstance(value, int):
        result = c_uamqp.int_value(value)
    elif isinstance(value, dict):
        wrapped_dict = c_uamqp.dict_value()
        for key, item in value.items():
            wrapped_dict[data_factory(key)] = data_factory(item)
        result = wrapped_dict
    elif isinstance(value, (list, set, tuple)):
        wrapped_list = c_uamqp.list_value()
        wrapped_list.size = len(value)
        for index, item in enumerate(value):
            wrapped_list[index] = data_factory(item)
        result = wrapped_list
    return result
