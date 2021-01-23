from flask import Flask, render_template, make_response, request, jsonify
from flask import abort, redirect, url_for
from jinja2 import Template
import os
import json
import werkzeug
from datetime import datetime
import subprocess
import time

import urllib

app = Flask(__name__)

# Authorization Blockchain API


def make_input(cc_name, func_name, args):
    # BCに投げる用の入力を生成する関数
    """
    :param cc_name string: Chaincode の名前
    :param func_name string: function の名前
    :param args list: 引数のリスト
    """
    PEER_PATH = "/home/ubuntu/project-bcauth/fabric-samples/bin/"
    PWD = "/home/ubuntu/project-bcauth/fabric-samples/test-network"
    cd = "cd {}; ".format(PWD)
    export_PATH = "export PATH={}/../bin:$PATH; ".format(PWD)
    export_CFG = "export FABRIC_CFG_PATH={}/../config/; ".format(PWD)
    export_CORE = "export CORE_PEER_TLS_ENABLED=true; export CORE_PEER_LOCALMSPID='Org1MSP'; export CORE_PEER_TLS_ROOTCERT_FILE={}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt; export CORE_PEER_MSPCONFIGPATH={}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;export CORE_PEER_ADDRESS=localhost:7051;".format(
        PWD, PWD)

    ret = cd + export_PATH + export_CFG + export_CORE + 'peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile {0}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n {1} --peerAddresses localhost:7051 --tlsRootCertFiles {2}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles {3}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c \'{{"function":"{4}","Args":{5}}}\''.format(
        PWD, cc_name, PWD, PWD, func_name, str(args).replace("\\\\", "\\").replace("'", '"'))
    # ret = cd + export_PATH + export_CFG + "ls $FABRIC_CFG_PATH"
    return ret


def terminal_interface(cmd):
    """
    :param cmd: str 実行するコマンド
    """
    proc = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    while True:
        line = proc.stdout.readline()
        if line:
            yield line
        if not line and proc.poll() is not None:
            break

    return line


def input_command(cmd):
    # BC にコマンドを投げる関数
    # 注：subprocess.check_output ではなぜか標準出力が取得できなかったので，
    # 以下の方法を試したらうまくいった．
    _output = []  # 標準出力を格納
    for line in terminal_interface(cmd):
        _output.append(line)
    time.sleep(3)  # コマンドの連続実行を阻止
    return _output


def interpret_command_output(_output):
    # BCから受け取った出力を解釈する関数
    try:
        # ... status:200 payload:"any_response" \n']
        # -> [200, payload:"any_response", \n']
        li = str(_output[0]).split('status:')[-1].split(' ')
        if li[0] == '200':
            output = li[1].replace('payload:', '').replace('\"', '')
            output_data = {
                'message': "success",
                'response': output
            }
        else:
            output = _output[0].decode('utf8').replace("'", '"')
            output_data = {
                'message': "error",
                'response': output
            }
        return output_data
    except:
        output_data = {
            'message': "error",
            'response': "Exception."
        }
        return output_data


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
    timestamp = request.form['timestamp']
    timeSig = request.form['timeSig']

    input = make_input("pat", "invoke", [roId, rsId, timestamp, timeSig])
    # print(input)
    """
    try:
        _output = subprocess.check_output(input)
    except:
        print("Error: pat_post().")
        """
    _output = input_command(input)
    output = interpret_command_output(_output)
    print(output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)
    param = {'uid': uid, 'pat': output['response']}
    qs = urllib.parse.urlencode(param)

    # return make_response(jsonify({"response": qs}))
    return redirect('http://eza1.ctiport.net:8080/reg-resource?' + qs, code=301)


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
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)
    res = output['response']
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
    # バイト列を文字列に変換
    body = body.decode('utf8').replace("'", '"')
    # 文字列をJSONに変換
    body = json.loads(body)

    resource_description = body['resource_description']
    print("resource_description: ", resource_description)
    resource_scopes = ""  # 初期化
    for i, e in enumerate(resource_description['resource_scopes']):
        resource_scopes = resource_scopes + e
        if i is not len(resource_description['resource_scopes'])-1:
            resource_scopes = resource_scopes + ", "
    description = resource_description['description']
    icon_uri = resource_description['icon_uri']
    name = resource_description['name']
    _type = resource_description['type']
    timestamp = body['timestamp']
    timeSig = body['timeSig']

    cc_name = "rreg"
    func_name = "invoke"
    args = [pat, resource_scopes, description,
            icon_uri, name, _type, timestamp, timeSig]
    # print("args: ", args)

    input = make_input(cc_name, func_name, args)
    # print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)
    res = {'resource_id': output['response']}

    return make_response(json.dumps({'response': res}), 200)
    # return render_template('rreg.html')

"""
@app.route('/rreg-list', methods=['post'])
def rreg_list():
    # pat から resource_id のリストを呼び出す
    
    :req_param PAT:
    
"""


@app.route('/rreg-call', methods=['post'])
def rreg_call():
    # resource_id から resource_description を呼び出す
    """
    :header Content-Type 'application/json':
    :header Authorization Bearer: PAT
    :req_param resourceId: リソース固有のID
    :res_param resourceDescription: リソースの情報
    # 内訳: resourceScopes[], description, iconUri, name, type
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
    # バイト列を文字列に変換
    body = body.decode('utf8').replace("'", '"')
    # 文字列をJSONに変換
    body = json.loads(body)
    # resource_id 呼び出し
    resource_id = body['resource_id']

    # CC に入力
    cc_name = "rreg"
    func_name = "query"
    args = [pat, resource_id]
    # print("args: ", args)

    input = make_input(cc_name, func_name, args)
    # print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    # rreg.go - query() の return の実装がミスっていた？のでこちらで処理する
    response = output['response'].split("\\\\")
    res = {}
    if response[1] == 'ResourceScopes':
        for i, e in enumerate(response):
            if e == 'ResourceScopes':
                res['resource_scopes'] = response[i+2]
            elif e == 'Description':
                res['description'] = response[i+2]
            elif e == 'IconUri':
                res['icon_uri'] = response[i+2]
            elif e == 'Name':
                res['name'] = response[i+2]
            elif e == 'Type':
                res['type'] = response[i+2]
            else:
                pass
    else:
        make_response(json.dumps({'response': "Error."}))
    print("response: ", response)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    res = {'name': res['name']}
    return make_response(json.dumps({'response': res}), 200)


@app.route('/policy')
def policy():
    # リソース ID に紐づくポリシーの設定画面を表示する
    if request.args.get('resource') != "" and request.args.get('rid') != "":
        resource = request.args.get('resource')
        rid = request.args.get('rid')
    else:
        return jsonify({'message': "error: no resource name or resource id"})

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
            <input type="hidden" name="rid" value={1}>
            <button type="submit" value="set-policy">set policy</button>
        </form>
        <br>
        <br>
        （手続き内容06）<br>
        リソース所有者は認可ポリシーを設定する．<br>
        このページでは，「クレームが発行されるエンドポイント」「クレームが示すエンティティ識別子」「Subjectの代理としてリソースへのアクセスを実行するクライアント識別子」の三要素をポリシーとして設定できる．<br>
        </p>

        <p><img src="/static/images/rreg06.png" width="841" height="500"></p>
    </body>

    </html>
    """.format(resource, rid)

    template = Template(html)

    return template.render()


@app.route('/policy', methods=['post'])
def policy_post():
    # ポリシーの設定を実行する
    rid = request.form['rid']
    print("rid: ", rid)
    iss = request.form['iss']  # クレームトークンの発行主
    sub = request.form['sub']  # クレームトークンの発行先（被検証者）
    aud = request.form['aud']  # クレームトークンの検証者
    if iss == "" or sub == "" or aud == "":
        return jsonify({'message': "error: iss or sub or aud is not configured"})

    cc_name = "policy"
    func_name = "invoke"
    args = [rid, iss, sub, aud]
    # print("args: ", args)
    input = make_input(cc_name, func_name, args)
    # print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    return render_template('policy.html', iss=iss, sub=sub, aud=aud)


@app.route('/perm', methods=['post'])
def perm():
    # チケットを発行する

    # PAT の呼び出し（方法は未定）
    # (ro01, rs) - rid = 08db20ba-2666-5b91-9bef-3d5b7d9138ae
    pat = "0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551"
    # (ro02, rs) - rid = 1c1f1d9f-051c-592f-bb06-5ec8cef664ba
    #pat = "0x23e6958b1f555b905ade2f915c8c64453bd9514c4e1750d995f17215cbc4"

    # ヘッダのチェック
    if not request.headers.get('Content-Type') == 'application/json':
        error_message = {
            'error': "not supported Content-Type"
        }
        return make_response(jsonify(error_message), 400)

    # リクエストボディの読み取り
    body = request.get_data().decode('utf8').replace("'", '"')
    body = json.loads(body)
    rid = body['resource_id']
    request_scopes = ""
    for i, e in enumerate(body['request_scopes']):
        request_scopes = request_scopes + e
        if i is not len(body['request_scopes'])-1:
            request_scopes = request_scopes + ":"
    dict = "{{" + rid + ",\\\"" + request_scopes + "\\\"" + "}}"
    timestamp = body['timestamp']
    timeSig = body['timeSig']

    # CC へ入力
    cc_name = "perm"
    func_name = "invoke"
    args = [pat, dict, timestamp, timeSig]
    input = make_input(cc_name, func_name, args)
    print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    res = {
        'ticket': output['response']
    }

    return make_response(json.dumps({'response': res}), 200)


@app.route('/token', methods=['post'])
def token():
    """
    :req_header Content-Type application/json:
    :req_param grant_type:
    :req_param ticket:
    :req_param claim_token:
    :req_param claim_token_format:
    :req_param timestamp:
    :req_param timeSig:
    :res_param RPT or Error(need_info):
    """
    # ヘッダのチェック
    if not request.headers.get('Content-Type') == 'application/json':
        error_message = {
            'error': "not supported Content-Type"
        }
        return make_response(jsonify(error_message), 400)

    # リクエストボディの読み取り
    body = request.get_data().decode('utf8').replace("'", '"')
    body = json.loads(body)
    grant_type = body['grant_type']
    ticket = body['ticket']
    # claim_token の有無を処理
    if 'claim_token' not in body:
        claim_token = ""
    else:
        claim_token = body['claim_token']

    if 'claim_token_format' not in body:
        claim_token_format = ""
    else:
        claim_token_format = body['claim_token_format']

    timestamp = body['timestamp']
    timeSig = body['timeSig']

    # CC へ入力
    cc_name = "token"
    func_name = "invoke"
    args = [grant_type, ticket, claim_token,
            claim_token_format, timestamp, timeSig]
    input = make_input(cc_name, func_name, args)
    print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    # token.go の return の実装がミスっていたのでこちらで処理する
    output = output['response'].split("\\\\")
    print(output)
    res = {}
    if len(output) == 1:
        res['token'] = output[0]
    elif output[1] == 'Error':
        for i, e in enumerate(output):
            if e == 'Error':
                res['Error'] = output[i+2]
            elif e == 'Ticket':
                res['Ticket'] = output[i+2]
            elif e == 'RedirectUser':
                res['RedirectUser'] = output[i+2]
            else:
                pass
    else:
        make_response(json.dumps({'response': "Error."}))
        

    return make_response(json.dumps({'response': res}), 200)


@app.route('/rqp-claims')
def claim():
    req_client_id = request.args.get('client_id')
    ticket = request.args.get('ticket')
    claims_redirect_uri = request.args.get('claims_redirect_uri')
    timestamp = request.args.get('timestamp')
    timeSig = request.args.get('timeSig')

    # CC へ入力
    cc_name = "claim"
    func_name = "invoke"
    args = [req_client_id, ticket, claims_redirect_uri, timestamp, timeSig]
    input = make_input(cc_name, func_name, args)
    #print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)
    res = output['response']  # ticket

    # /authen へリダイレクト
    param = {
        'ticket': res,
        'claims_redirect_uri': claims_redirect_uri,
        'client_id': req_client_id,
        'timestamp': timestamp,
        'timeSig': timeSig
    }
    qs = urllib.parse.urlencode(param)

    return redirect(url_for('authen') + '?' + qs, code=301)


@app.route('/authen')
def authen():
    """
    :req_param ticket: パーミッションチケット
    """
    # パラメータを受け取る
    ticket = request.args.get('ticket')
    claims_redirect_uri = request.args.get('claims_redirect_uri')
    client_id = request.args.get('client_id')
    timestamp = request.args.get('timestamp')
    timeSig = request.args.get('timeSig')

    # ticket を検証し，正しければ処理を継続(invokeAuthen() - claim.go)
    cc_name = "claim"
    func_name = "invokeAuthen"
    args = [ticket, timestamp, timeSig]
    input = make_input(cc_name, func_name, args)
    #print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    res = output['response']  # ticket

    # 認証処理用のフォームを返す
    html = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0
    Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    <html xmlns="http://www.w3.org/1999/xhtml">

    <head>
        <title></title>
    </head>

    <body>
        <h1>Authorization Blockchain API</h1>
        <h2>認証フォーム</h2>
        <p>認証処理を実施します．</p>
        <br>
        <form action="/authen" method="post">
            <p>ユーザ ID:   <input type="text" name="uid"></p>
            <p>パスワード:  <input type="password" name="password"></p>
            <input type="hidden" name="ticket" value={0}>
            <input type="hidden" name="client_id" value={1}>
            <input type="hidden" name="claims_redirect_uri" value={2}>
            <button type="submit" value="authen">submit</button>
        </form>
        <br>
        <br>
        （手続き内容10）<br>
        認可ブロックチェーンはRqP及びクライアントがリソースに紐付けられる認可ポリシーを満たすか検証するために，RqPに対し認証情報を要求する．<br>
        RqPは認可ブロックチェーンに対し，自身の認証情報を送信する．<br>
        認可ブロックチェーンによる認証情報の検証が正常に終了すると，RqP及びクライアントの認証情報を格納したクレームトークンが発行される．<br>
        </p>

        <p><img src="/static/images/authz03.png" width="841" height="500"></p>
    </body>

    </html>
    """.format(res, client_id, claims_redirect_uri)

    template = Template(html)

    return template.render()


@app.route('/authen', methods=['post'])
def authen_post():
    """
    :req_param uid: ユーザ ID
    :req_param password: パスワード
    :req_param ticket: パーミッションチケット
    :req_param client_id: クライアント ID
    """
    # パラメータを受け取る
    uid = request.form['uid']
    password = request.form['password']
    ticket = request.form['ticket']
    client_id = request.form['client_id']
    claims_redirect_uri = request.form['claims_redirect_uri']

    # 認証情報を検証
    dir = './authenDB/'
    file = 'user.txt'
    path = dir + file
    with open(path, encoding='utf-8') as f:
        li = f.readlines()
    print("li: ", li)
    dict = {}  # { uid : password }
    for i in range(len(li)):
        dict[li[i].strip().split(':')[0]] = li[i].strip().split(':')[1]
    try:
        _password = dict[uid]
        if password != _password:
            return make_response(jsonify({'error': "user id or password is invalid."}), 400)
    except:
        return make_response(jsonify({'error': "user id may not exists."}), 400)

    # claim_token を生成する
    claim_token = {
        'iss': "http://tff-01.ctiport.net:8888/authen",
        'sub': uid,
        'aud': client_id
    }

    token_endpoint = 'http://tff-01.ctiport.net:8888/token'

    claim_token_str = json.dumps(claim_token).replace(" ", "").replace('"', '')

    # ticket と claim_token を返す
    param = {
        'ticket': ticket,
        'claim_token': claim_token_str,
        'token_endpoint': token_endpoint
    }
    qs = urllib.parse.urlencode(param)

    return redirect(claims_redirect_uri + '?' + qs, 301)


@app.route('/intro', methods=['post'])
def intro():
    # ヘッダのチェック
    if not request.headers.get('Content-Type') == 'application/json':
        error_message = {
            'error': "not supported Content-Type"
        }
        return make_response(jsonify(error_message), 400)

    # リクエストボディの読み取り
    body = request.get_data().decode('utf8').replace("'", '"')
    body = json.loads(body)
    rpt = body['access_token']

    # PAT の呼び出し（方法は未定）
    # (ro01, rs) - rid = 08db20ba-2666-5b91-9bef-3d5b7d9138ae
    pat = "0xddb5ab8c5405830359d2af4ec8d4bdf27bc4b8ee7d20f64ec1a71a634e551"

    # rpt を検証する
    cc_name = "intro"
    func_name = "invoke"
    args = [pat, rpt]
    input = make_input(cc_name, func_name, args)
    #print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    if output['message'] == "error":
        error_message = {
            'error': output['response']
        }
        return make_response(jsonify(error_message), 400)

    # return の実装ミスを処理
    res = output['response'].replace("\\", "").replace("{", "{\"").replace("}", "\"}")
    res = res.replace(":", "\":\"").replace(",", "\",\"").replace("\"[", "[").replace("]\"", "]")
    # ResourceScopes キーのリストのみ中身を文字列化する
    res = res.replace('"ResourceScopes":[', '"ResourceScopes":["').replace('],"Expire"', '"],"Expire"')
    res = json.loads(res)

    return make_response(json.dumps({'response': res}), 200)



if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True, host='0.0.0.0', port=8888)
