from flask import Flask, render_template, make_response, request, jsonify
from flask import abort, redirect, url_for
import os
import werkzeug
from datetime import datetime

import urllib

app = Flask(__name__)

# Authorization Blockchain API


def make_input():
    # BCに投げる用の入力を生成する関数
    return None


def interpret_command_output():
    # BCから受け取った出力を解釈する関数
    return None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/pat')
def pat():
    return render_template('pat.html')


@app.route('/pat', methods=['post'])
def pat_post():
    """
    :req_param uid: RS における RO のユーザID
    :req_param roId: AB における RO に固有の ID
    :req_param rsId: AB における RS に固有の ID
    :res_param uid: RS における RO のユーザID
    :res_param pat: 発行した PAT
    """
    uid = request.form['uid']
    roId = request.form['roId']
    rsId = request.form['rsId']

    input = make_input(roId, rsId)
    _output = command(input)
    output = interpret_command_output(_output)
    param = {'uid': uid, 'pat': output}
    #param = {'q': roId + " " + rsId}
    qs = urllib.parse.urlencode(param)

    return redirect('http://eza1.ctiport.net:8080/reg-resource?' + qs, code=301)
    # return redirect('https://www.google.com/search?' + qs, code=301)


@app.route('/rreg')
def rreg_list():
    # 登録したリソースの一覧を表示する
    """
    :header Authorization Bearer: PAT
    """
    # header をチェック
    if not request.headers.get('Content-Type') == 'application/json':
        error_message = {
            'error': 'not supported Content-Type'
        }
        return make_response(jsonify(error_message), 400)
    try:
        header_authz = request.headers.get('Authorization')
        bearer = header_authz.split('Bearer ')[-1]
    except:
        error_message = {
            'error': 'bearer token is needed'
        }
        return make_response(jsonify(error_message), 400)

    pat = bearer

    input = make_input(pat)
    _output = command(input)
    output = interpret_command_output(_output)
    res = output
    return render_template('rreg.html', res=res)


@app.route('/rreg', methods=['post'])
def rreg_create():
    # リソースを登録する
    """
    :header Content-Type 'application/json':
    :header Authorization Bearer: PAT
    :req_param resourceDescription: リソースの情報
    # 内訳: resourceScopes[], description, iconUri, name, type
    :res_param resourceId: リソース固有のID
    """
    # header をチェック
    if not request.headers.get('Content-Type') == 'application/json':
        error_message = {
            'error': 'not supported Content-Type'
        }
        return make_response(jsonify(error_message), 400)
    try:
        header_authz = request.headers.get('Authorization')
        bearer = header_authz.split('Bearer ')[-1]
    except:
        error_message = {
            'error': 'bearer token is needed'
        }
        return make_response(jsonify(error_message), 400)

    pat = bearer

    # body を読み取る
    body = request.get_data()
    resource_description = body.resource_description
    input = make_input(pat, resource_description)
    _output = command(input)
    output = interpret_command_output(_output)
    res = {'resource_id': output.resourceId}

    return jsonify({'res': res})
    # return render_template('rreg.html')


@app.route('/policy')
def policy():
    # リソース ID に紐づくポリシーの設定画面を表示する
    if request.args.get('resource') != "" and request.args.get('rid') != "":
        resource = request.args.get('resource')
        rid = request.args.get('rid')
    else:
        return jsonify({'message': "error: no resource or resource id"})

    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 
    Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title></title>
    </head>

    <body>
        <h1>Authorization Blockchain API</h1>
        <h2>ポリシー設定エンドポイント</h2>
        <p>Resource: {0} に紐づくポリシーを設定します．</p>
        <br>
        <form action="/policy" method="post">
            <p>Issuer:   <input type="text" name="iss"></p>
            <p>Subject:  <input type="text" name="sub"></p>
            <p>Audience: <input type="text" name="aud"></p>
            <input type="hidden" name="rid" value={1}">
            <button type="submit" value="set-policy">set policy</button>
        </form>
    </body>

    </html>
    """.format(resource, rid)

    return render_template('policy.html')


@app.route('/policy', methods=['post'])
def policy_post():
    # ポリシーの設定を実行する
    rid = request.form['rid']
    iss = request.form['iss']
    sub = request.form['sub']
    aud = request.form['aud']
    if iss == "" or sub == "" or aud == "":
        return jsonify({'message': "error: iss or sub or aud is not configured"})

    input = make_input(rid, iss, sub, aud)
    _output = command(input)
    output = interpret_command_output(_output)
    return jsonify({'message': "successfully configured."})


@app.route('/perm')
def perm():
    return None


@app.route('/token')
def token():
    return None


@app.route('/claim')
def claim():
    return None


@app.route('/intro')
def intro():
    return None


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8888)
