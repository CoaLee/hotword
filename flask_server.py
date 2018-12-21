from flask import Flask, request, make_response, jsonify
from slacker import Slacker
import requests, json
from slackclient import SlackClient
import process, crawling

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# 슬랙 토큰으로 객체 생성
token = "xoxb-503818135714-509602121223-fTOD60tiu26We4Xd5Km6WGPX"
slack_verification = "869x6D9L8QjN08ciUCRnyodW"
slack = Slacker(token)

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
        if 'keyword' in result_df:
            keyword = result_df['keyword']

        # 다음 뉴스 카테고리와 영문(url주소)명
        category_dict = {"사회": "society", "정치": "politics", "경제": "economic", "국제": "foreign",
            "문화": "culture", "연예": "entertain", "스포츠": "sports", "IT": "digital", "칼럼": "editorial",
            "보도자료": "press"}

        if intent == 'category':
            # 카테고리 검색 -> 다음 뉴스 카테고리 검색
            if keyword in category_dict:
                category_name = "category_{0}".format(category_dict[keyword])
                process.process_main(category_name)

                slack.chat.post_message(channel, speech)
                slack.files.upload('img_wordcloud/{0}.png'.format(category_name), channels=channel)
            # 키워드 검색 -> 조선일보 검색 결과
            else:
                process.process_search(keyword)
                slack.chat.post_message(channel, speech)
                slack.files.upload('img_wordcloud/keyword_result.png', channels=channel)

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
    print(data_receive.items())
    result = {
        "speech": data_receive['result']['fulfillment']['speech'],
        "intent": data_receive['result']['metadata']['intentName'],

    }
    if 'any' in data_receive['result']['parameters']:
        result["keyword"] = data_receive['result']['parameters']['any']

    return result


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
