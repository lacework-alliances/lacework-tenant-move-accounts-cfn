#
# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import json
import logging
import os
import urllib3
from crhelper import CfnResource

from aws import send_cfn_fail, send_cfn_success
from honeycomb import send_honeycomb_event
from lacework import setup_initial_access_token,  get_lacework_environment_variables, get_account_from_url, \
    move_bulk_lw_cloud_accounts

HONEY_API_KEY = "$HONEY_KEY"
DATASET = "$DATASET"
BUILD_VERSION = "$BUILD"

http = urllib3.PoolManager()

LOGLEVEL = os.environ.get('LOGLEVEL', logging.INFO)
logger = logging.getLogger()
logger.setLevel(LOGLEVEL)

helper = CfnResource(json_logging=False, log_level="INFO", boto_level="CRITICAL", sleep_on_delete=15)


def lambda_handler(event, context):
    logger.info("move.lambda_handler called.")
    logger.info(json.dumps(event))
    try:
        if "RequestType" in event: helper(event, context)
    except Exception as e:
        helper.init_failure(e)


@helper.create
@helper.update
def create(event, context):
    logger.info("move.create called.")
    logger.info(json.dumps(event))

    lacework_url = os.environ['lacework_url']
    lacework_account_name = get_account_from_url(lacework_url)
    from_tenant_name = os.environ['from_tenant_name']
    to_tenant_name = os.environ['to_tenant_name']
    aws_accounts = os.environ['aws_accounts']
    access_key_id = os.environ['access_key_id']
    secret_key = os.environ['secret_key']
    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "move started",
                         "", get_lacework_environment_variables())

    logger.info(
        "Lacework URL: {}, Lacework account: {}".format(
            lacework_url,
            lacework_account_name))

    try:
        access_token = setup_initial_access_token(lacework_url, access_key_id, secret_key)

        move_bulk_lw_cloud_accounts(lacework_url, aws_accounts, from_tenant_name, to_tenant_name, access_token)

    except Exception as move_exception:
        send_cfn_fail(event, context, "Move failed {}.".format(move_exception))
        return None

    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "move completed", "")
    send_cfn_success(event, context)
    return None


@helper.delete
def delete(event, context):
    logger.info("move.delete called.")
    lacework_url = os.environ['lacework_url']
    lacework_account_name = get_account_from_url(lacework_url)

    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "delete started", "")

    send_honeycomb_event(HONEY_API_KEY, DATASET, BUILD_VERSION, lacework_account_name, "delete completed", "")
    send_cfn_success(event, context)
    return None
