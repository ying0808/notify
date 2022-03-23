import requests
from flask import Flask, request
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect(database='d8j8ci273kope7',user='fcxvwdfzmxmtck',password='45b0956d0daf63dceb105ef92756d73d371a010c4c4b4295865e5ce1a04c4084',host='ec2-44-194-167-63.compute-1.amazonaws.com',port='5432')
app.conn = conn
'''
使用者訂閱網址：
https://notify-bot.line.me/oauth/authorize?response_type=code&client_id=i1luZv2hDQsfgAScKoOS2v&redirect_uri=https://testmypostgre.herokuapp.com/&scope=notify&state=NO_STATE
'''


def getNotifyToken(AuthorizeCode):
    body = {
        "grant_type": "authorization_code",
        "code": AuthorizeCode,
        "redirect_uri": 'https://testmypostgre.herokuapp.com/',
        "client_id": 'i1luZv2hDQsfgAScKoOS2v',
        "client_secret": 'YDWMinYnO4uITeIwlTUbrYoblTucmvZK67QggmT9OkU'
    }
    r = requests.post("https://notify-bot.line.me/oauth/token", data=body)
    return r.json()["access_token"]


def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify",
                      headers=headers, data=payload)
    return r.status_code


    
def insert_table(token):
    
        cursor = app.conn.cursor()
        insert_query = """ INSERT INTO token (token) VALUES (%s)"""
        cursor.execute(insert_query,(token,))
        app.conn.commit()
        cursor.close()
        app.conn.close()
        return token


@app.route('/', methods=['POST', 'GET'])
def hello_world():
    authorizeCode = request.args.get('code')
    if authorizeCode == None:
        return f"請重新連接"
    token = getNotifyToken(authorizeCode)
    insert_table(token)
    lineNotifyMessage(token, "恭喜你連動完成")
    return f"恭喜你，連動完成"


if __name__ == '__main__':
    app.run()