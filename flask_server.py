from flask import Flask, request, make_response, jsonify
from slacker import Slacker
import requests, json
from slackclient import SlackClient
import process

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 슬랙 토큰으로 객체 생성
token = "xoxb-503818135714-509602121223-JU7TqOGdGsI4JwufhOOAldJw"
slack_verification = "869x6D9L8QjN08ciUCRnyodW"
slack = Slacker(token)
sc = SlackClient(token)

@app.route('/')
def index():
    return "Hello, I'm ready"

@app.route('/listening', methods=["GET", "POST"])
def listening():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":
                                                                 "application/json"
                                                             })

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return _event_handler(event_type, slack_event)

    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})

def _event_handler(event_type, slack_event):
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]

        result_df = _get_answer_from_DF(text[13:], 'random_session')

        speech = result_df['speech']
        intent = result_df['intent']

        result_process = " result "
        print(intent)
        if intent in ['category', 'category_society']:
            result_process = _call_process()
            print(result_process)

        process.process_main("category_society")
        slack.chat.post_message(channel, '{0}\n\n{1}'.format(speech, result_process))
        slack.files.upload('category_society.png', channels=channel)
        '''
        sc.api_call(
            "chat.postMessage",
            channel=channel,
            text='{0}\n\n{1}'.format(speech, result_process)
        )
        '''
        print('{0}\n\n{1}'.format(speech, result_process))

        return make_response("App mention message has been sent", 200)
    else :
        # ============= Event Type Not Found! ============= #
        # If the event_type does not have a handler
        message = "You have not added an event handler for the %s" % event_type
        # Return a helpful error message
        return make_response(message, 200, {"X-Slack-No-Retry": 1})

def _get_answer_from_DF(slack_msg, user_key):
    data_send = {
        'query': slack_msg,
        'sessionId': user_key,
        'lang': 'ko',
    }

    data_header = {
        'Authorization': 'Bearer 22c41598e8464addbc40892602a5ea3d',
        'Content-Type': 'application/json; charset=utf-8'
    }

    dialogflow_url = 'https://api.dialogflow.com/v1/query?v=20150910'
    res = requests.post(dialogflow_url, data=json.dumps(data_send), headers=data_header)

    if res.status_code != requests.codes.ok:
        return '오류가 발생했습니다.'

    data_receive = res.json()
    result = {
        "speech": data_receive['result']['fulfillment']['speech'],
        "intent": data_receive['result']['metadata']['intentName']
    }

    return result

# Wrapper
def _call_crawler():
    return "crawler called"

# Wrapper
def _call_process():
    return _call_crawler() + "->" + "process processed"

if __name__ == '__main__':
    app.run(host='0.0.0.0')

'''Slacker example
# 메시지 전송 (#채널명, 내용)
slack.chat.post_message('#day4', 'Slacker 파일 업로드 테스트')

# 파일 업로드 (파일 경로, 채널명)
# slack.files.upload('dog.png', channels="#day4")

# 사용자 리스트 반환
response = slack.users.list()
users = response.body['members']
# print(users)
'''
