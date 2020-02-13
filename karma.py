import slack
import time
import datetime
import logging
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mytoken import token
from dbsetup import Message, Base


def post_message(slack_client, mychannel, message):
    slack_client.chat_postMessage(
        channel='#' + mychannel,
        text=message)


def add_ts_to_db(timestamp):
    """
    Add a new Timestamp to the database
    :param timestamp: the time stamp to add to the database
    """
    if session.query(Message).filter_by(timestamp=timestamp).count():
        return
    new_ts = Message(timestamp=timestamp)
    session.add(new_ts)
    session.commit()


def get_latest_ts_from_db():
    """
    Get the latest TS in the database
    :return: the TS object with the latest time stamp
    """
    obj = session.query(Message).order_by(Message.timestamp.desc()).first()
    return obj


def get_channel_id(name):
    list = slack_client.channels_list()
    for each in list.data.get('channels'):
        if each.get('name') == name:
            return each.get('id')
    return None


# DB Setup variables
engine = create_engine('sqlite:///db.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

logging.basicConfig()
slack_client = slack.WebClient(token=token)
mychannel = 'test-channel'
id = get_channel_id(mychannel)
if not id:
    sys.exit(1)
while True:
    post_message(slack_client, mychannel, "this is a message")
    if id:
        ts = get_latest_ts_from_db()
        if ts is not None:
            ts = ts.timestamp.timestamp()
            l = slack_client.channels_history(channel=id, oldest=str(ts) + '01', inclusive="false")
            for each in l['messages']:
                add_ts_to_db(datetime.datetime.fromtimestamp(float(each['ts'])))
        else:
            l = slack_client.channels_history(channel=id, inclusive="false")
            for each in l['messages']:
                add_ts_to_db(datetime.datetime.fromtimestamp(float(each['ts'])))
    time.sleep(2)
