import slack
import time
import logging
from mytoken import token
logging.basicConfig()
slack_client = slack.WebClient(token=token)
id = None
mychannel = 'test-channel'
list = slack_client.channels_list()
for each in list.data.get('channels'):
    if each.get('name') == mychannel:
        id = each.get('id')
while True:
    response = slack_client.chat_postMessage(
        channel='#' + mychannel,
        text="This is a message")
    if id:
        l = slack_client.channels_history(channel=id)
        print(str(l))
        print('----------')
    time.sleep(2)

