import os
import time
from slackclient import SlackClient

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")
BOT_ID = "U2TQ1DR26"
BOT_TOKEN = "xoxb-95817467074-KxD3DsTRgZAPEchJkWM2Xs6f"

# constants
AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = "go home dan!"

good_pictures = ["hoagie.png",
                "Mixed-Sandwich-Platter1.jpg",
                "penne-puttanesca-sauce.jpg",
                "PennePuttanesca.JPG",
                "Sandwich-AvocadoBLT.jpg",
                "tomme.jpg"]
base_url = "http://dantrim.web.cern.ch/dantrim/go_home_dan/images/"
last_image_idx = 0


# instantiates Slack and Twilio clients
#slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
slack_client = SlackClient(BOT_TOKEN)

def handle_command(command, channel):
    global last_image_idx
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    #response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #           "* command with numbers, delimited by spaces."
    response = "I only respond to '" + EXAMPLE_COMMAND + "' commands." + \
                " It is a lonely life, but one I must lead. Sandwiches."
    #if command.startswith(EXAMPLE_COMMAND):
    #    response = "Sure...write some more code then I can do that!"
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                      text=response, as_user=True)
    image_idx = 0
    if last_image_idx == len(good_pictures)-1 :
        image_idx = 0
    else :
        image_idx = last_image_idx + 1
    print "selecting image at index %d : %s%s"%(image_idx, base_url, good_pictures[int(image_idx)])
    slack_client.api_call("chat.postMessage", channel=channel,
                            text = "Time to go home, Dan. Look what is waiting for you there! Hmmm... Impossible to resist.",
                            attachments='[{"title":"delicious", "image_url":"%s%s"}]'%(base_url, good_pictures[int(image_idx)]))
    last_image_idx = image_idx
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                        text = "Time to go home, Dan. Look what is waiting for you there! Hmmm... Sandwich... Impossible to resist.",
    #                        attachments='[{"title":"delicious", "image_url":"https://saladworks.com/sites/default/files/Sandwich-AvocadoBLT.jpg"}]')


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
