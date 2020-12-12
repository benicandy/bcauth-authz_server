from flask import Flask, render_template, make_response, request, jsonify
from flask import abort, redirect, url_for
from jinja2 import Template
import os, json
import werkzeug
from datetime import datetime
import subprocess

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
    export_CORE = "export CORE_PEER_TLS_ENABLED=true; export CORE_PEER_LOCALMSPID='Org1MSP'; export CORE_PEER_TLS_ROOTCERT_FILE={}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt; export CORE_PEER_MSPCONFIGPATH={}/organizations/peerOrganizations/org1.example.com/users/Admin@org1.example.com/msp;export CORE_PEER_ADDRESS=localhost:7051;".format(PWD, PWD)

    ret = cd + export_PATH + export_CFG + export_CORE + 'peer chaincode invoke -o localhost:7050 --ordererTLSHostnameOverride orderer.example.com --tls --cafile {0}/organizations/ordererOrganizations/example.com/orderers/orderer.example.com/msp/tlscacerts/tlsca.example.com-cert.pem -C mychannel -n {1} --peerAddresses localhost:7051 --tlsRootCertFiles {2}/organizations/peerOrganizations/org1.example.com/peers/peer0.org1.example.com/tls/ca.crt --peerAddresses localhost:9051 --tlsRootCertFiles {3}/organizations/peerOrganizations/org2.example.com/peers/peer0.org2.example.com/tls/ca.crt -c \'{{"function":"{4}","Args":{5}}}\''.format(
        PWD, cc_name, PWD, PWD, func_name, str(args).replace("'", '"'))
    #ret = cd + export_PATH + export_CFG + "ls $FABRIC_CFG_PATH"
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
    return _output


def interpret_command_output(_output):
    # BCから受け取った出力を解釈する関数
    try:
        # ...status:200 payload:"any_response" \n']
        # -> [200, payload:"any_response", \n']
        li = str(_output[0]).split('status:')[-1].split(' ')
        if li[0] == '200':
            output = li[1].replace('payload:', '').replace('\"', '')
        else:
            output = _output[0].decode('utf8').replace("'", '"')
        return output
    except:
        return "Error: exception."


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
    timestamp = "1595230979"
    timeSig = "vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="

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
    param = {'uid': uid, 'pat': output}
    qs = urllib.parse.urlencode(param)

    # return make_response(jsonify({"message": qs}))
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
    # バイト列を文字列に変換
    body = body.decode('utf8').replace("'", '"')
    # 文字列をJSONに変換
    body = json.loads(body)

    resource_description = body['resource_description']
    print("resource_description: ", resource_description)
    resource_scopes = ""
    for i, e in enumerate(resource_description['resource_scopes']):
        resource_scopes = resource_scopes + e
        if i is not len(resource_description['resource_scopes'])-1:
            resource_scopes = resource_scopes + ", "
    description = resource_description['description']
    icon_uri = resource_description['icon_uri']
    name = resource_description['name']
    _type = resource_description['type']
    timestamp = "1595230979"
    timeSig = "vF9Oyfm+G9qS4/Qfns5MgSZNYjOPlAIZVECh2I5Z7HHgdloy5q7gJoxi7c1S2/ebIQbEMLS05x3+b0WD0VJfcWSUwZMHr3jfXYYwbeZ1TerKpvfp1j21nZ+OEP26bc28rLRAYZsVQ4Ilx7qp+uLfxu9X9x37Qj3n0CI2TEiKYSSYDQ0bftQ/3iWSSoGjsDljh9bKz1eVL911KeUGO+t/9IkB6LtZghdbIlnGISbgrVGoEOtGHi0t8uD2Vh/CRyBe+XnQV3HQtkjddLQitAesKTYunK1Ctia3x7klVjRH9XiJ11q6IbR8gz7rchdHYZe6HP+w/LyWMS5z6M26AXQrVw=="

    cc_name = "rreg"
    func_name = "invoke"
    #args = "[\"" + pat + "\", \"" + resource_description.replace("'", '"').replace('"', '\\"') + "\"]"
    args = [pat, resource_scopes, description, icon_uri, name, _type, timestamp, timeSig]
    #print("args: ", args)

    input = make_input(cc_name, func_name, args)
    #print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)
    res = {'resource_id': output}

    return make_response(json.dumps({'response': res}), 200)
    # return render_template('rreg.html')


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
    #print("args: ", args)
    input = make_input(cc_name, func_name, args)
    #print("input: ", input)
    _output = input_command(input)
    output = interpret_command_output(_output)
    print("output: ", output)

    return jsonify({'message': output})


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
