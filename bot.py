from slackclient import SlackClient
import re
import time

# instantiate Slack client
slack_client = SlackClient('你的Token') # 在Slack API页面内获取

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXANPLE_COMMAND = "我是不是很帅" # 这里就是命令关键词，bot从Slack RTM 接收信息，并匹配，匹配成功就执行相应的if。
MENTION_REGEX = "(.*)"
def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
            message = parse_direct_mention(event["text"])
            return message, event["channel"]
    return None, None

def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1).strip()) if matches else (None)

def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "啊~  没有找到相应的指令呢 ⊂((・x・))⊃ " 
	
    # Finds and executes the given command, filling in response
    response = None
    # This is where you start to implement more commands!
    #这里开始
    if command.startswith(EXANPLE_COMMAND): # 这一块就是命令执行部分。
        response = """是的，是的。"""
    #这里结束 
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response  or default_response
    )

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        while True:
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
    else:
        print("Connection failed. Exception traceback printed above.")

