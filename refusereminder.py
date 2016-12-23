#!/usr/bin/env python
from __future__ import print_function

import boto3
import json
import os

from mkerefuse.refuse import RefuseQuery
from mkerefuse.refuse import RefuseQueryAddress


DEFAULT_SNS_TOPIC = 'mke-trash-pickup'
"""Default topic to notify for pickup changes"""

DEFAULT_S3_BUCKET = 'mke-trash-pickup'
"""Default S3 bucket name for storing persistent data"""

DEFAULT_S3_PREFIX = ''
"""Default S3 key prefix for persistent data"""

DEFAULT_S3_KEY = 'mke-trash-pickup.json'
"""Default S3 key for persistent data"""


def get_sns_topic_arn(topic_name, aws_region=None, aws_account_num=None):
    if aws_region is None:
        aws_region = boto3.session.Session().region_name

    if aws_account_num is None:
        aws_account_num = boto3.client('sts').get_caller_identity()['Account']

    return ":".join([
        "arn",
        "aws",
        "sns",
        aws_region,
        aws_account_num,
        topic_name])


def notify_pickup_change(pickup, sns_topic):
    """
    Produces a notification for a garbage pickup change
    """
    print("Notifying SNS: {}".format(sns_topic.arn))

    notify_msg = """
Garbage: {garbage}
Recycle (After): {recycle_after}
Recycle (Before): {recycle_before}""".format(
        garbage=pickup.next_pickup_garbage,
        recycle_after=pickup.next_pickup_recycle_after,
        recycle_before=pickup.next_pickup_recycle_before).strip()

    print("\n{}\n".format(notify_msg))
    return
    sns_topic.publish(
        Subject='Garbage Day Update',
        Message=notify_msg)


def lambda_handler(event, context):
    """
    Detects garbage day changes & updates them
    """

    # Compose the address
    address = RefuseQueryAddress(
        house_number=event['house_number'],
        direction=event['direction'],
        street_name=event['street_name'],
        street_type=event['street_type'])
    print("Querying address: {num} {d} {name} {t}".format(
        num=address.house_number,
        d=address.direction,
        name=address.street_name,
        t=address.street_type))

    # Query for the collection schedule
    pickup = RefuseQuery.Execute(address)

    # Create an S3 resource for fetching/storing persistent data
    s3 = boto3.resource('s3')

    # Attempt reading the last pickup information
    s3_bucket = event.get('s3_bucket', DEFAULT_S3_BUCKET)
    s3_key = os.path.join(
        event.get('s3_prefix', DEFAULT_S3_PREFIX),
        event.get('s3_key', DEFAULT_S3_KEY)).lstrip('/')
    s3_object = s3.Object(s3_bucket, s3_key)

    last_data = json.loads('{}')
    try:
        print("Loading previous pickup data from s3://{b}/{k}".format(
            b=s3_object.bucket_name,
            k=s3_object.key))
        last_data = json.loads(s3_object.get()['Body'].read().decode('utf-8'))

    except Exception as e:
        # Failed to load old data for some reason
        # Ignore it and assume a change in dates
        print("Failed to load previous pickup data")
        print(e)

    # Overwrite previous pickup data with the new data
    s3_object.put(Body=json.dumps(pickup.to_dict()))

    # If the information differs, notify of the changes
    if last_data != pickup.to_dict():
        print("Pickup change detected")
        sns = boto3.resource('sns')

        notify_pickup_change(
            pickup,
            sns_topic=sns.Topic(
                get_sns_topic_arn(event.get('sns_topic', DEFAULT_SNS_TOPIC))))
