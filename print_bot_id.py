import os
from slackclient import SlackClient

BOT_NAME = 'sandwichbot'

slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


if __name__ == "__main__" :
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok') :
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users :
            if 'name' in user and user.get('name') == BOT_NAME :
                #msg = "BOT ID for '%s' is "%user['name'], user.get('id')
                print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
                #print msg
    else :
        print "Could not find bot user with name %s"%BOT_NAME
