from flask import Flask
from slacker import Slacker

app = Flask(__name__)

# 슬랙 토큰으로 객체 생성
token = "xoxb-503818135714-509602121223-xBDZOPzJ76fRRVmnAHDaYquv"
slack = Slacker(token)

@app.route('/')
def index():
    return "Hello, I'm ready"

@app.route('/listening', methods=["GET", "POST"])
def listening():
    pass

def _event_handler(event_type, slack_event):
    pass

def _get_intent(slack_msg, user_key):
    pass


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
