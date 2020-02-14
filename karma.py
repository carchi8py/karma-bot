import slack
import time
import datetime
import logging
import sys
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mytoken import token
from dbsetup import Message, Base


class KarmaBot(object):
    def __init__(self):
        engine = create_engine('sqlite:///db.db')
        Base.metadata.bind = engine
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()

        logging.basicConfig()
        self.mychannel = 'newtest'
        self.slack_client = slack.WebClient(token=token)

    def post_message(self, message):
        print('#'+self.mychannel)
        print(message)
        self.slack_client.chat_postMessage(
            channel='#'+self.mychannel,
            text=message
        )

    def add_ts_to_db(self, timestamp):
        """
        Add a new Timestamp to the database
        :param timestamp: the time stamp to add to the database
        """
        if self.session.query(Message).filter_by(timestamp=timestamp).count():
            return
        new_ts = Message(timestamp=timestamp)
        self.session.add(new_ts)
        self.session.commit()

    def get_latest_ts_from_db(self):
        """
        Get the latest TS in the database
        :return: the TS object with the latest time stamp
        """
        obj = self.session.query(Message).order_by(Message.timestamp.desc()).first()
        return obj

    def get_channel_id(self):
        list = self.slack_client.channels_list()
        for each in list.data.get('channels'):
            if each.get('name') == self.mychannel:
                return each.get('id')
        return None

    def add_new_ts_to_db(self, id, ts):
        if ts is not None:
            ts = ts.timestamp.timestamp()
            history = self.slack_client.channels_history(channel=id, oldest=str(ts) + '01', inclusive="false")
            for each in history['messages']:
                self.add_ts_to_db(datetime.datetime.fromtimestamp(float(each['ts'])))
        else:
            history = self.slack_client.channels_history(channel=id, inclusive="false")
            for each in history['messages']:
                self.add_ts_to_db(datetime.datetime.fromtimestamp(float(each['ts'])))
        return history

    def parse_karma(self, message):
        message_text = message['text']
        # First check to see if we have a username (this will only work for 1 user in a message)
        if "@" in message_text:
            username = message_text.split('@')[1]
            print(username)
        if "+" in message_text:
            self.post_message("Plus Karma")
        if '-' in message_text:
            self.post_message("Minus Karma")

    def run(self):
        id = self.get_channel_id()
        if not id:
            sys.exit(1)
        while True:
            # Get the latest time stamp from the database so we don't run on the same message
            ts = self.get_latest_ts_from_db()
            if ts:
                print(ts.timestamp.timestamp())
            # record the latest message to the database and show the history
            history = self.add_new_ts_to_db(id, ts)
            # If there is a message we want to parse it to see if they want to add or remove karma
            if history['messages']:
                for message in history['messages']:
                    self.parse_karma(message)

            print('-----')

            time.sleep(2)

def main():
    ''' Create object and call apply '''
    obj_aggr = KarmaBot()
    obj_aggr.run()


if __name__ == '__main__':
    main()
