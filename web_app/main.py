import sqlite3
import json
import time
# Flaskとrender_templateをインポート
from flask import Flask, render_template, request, jsonify
from waitress import serve
# 半角カナを全角へ全角英字を半角英字へ
import unicodedata

# Flaskオブジェクトの生成
# 第二引数を変更でhtmlファイルのパス名が変更可能(こうしないとtemplatesしか受け取れない)
app = Flask(__name__, template_folder= "html")
# 文字化け防止
app.config["JSON_AS_ASCII"] = False

# 辞書型へ変換する関数
def dict_factory(cursor, row):
   d = {}
   for idx, col in enumerate(cursor.description):
       d[col[0]] = row[idx]
   return d

# form入力(HTML)とデータベースを一致させる, カラム名とキー名が一致する
def match_DB2HTML(request):
    input_request_dict = {\
        'ID': request.form.getlist('ID'), \
        'Gun_MajorName': request.form.getlist('Gun_MajorName'), \
        'Country': request.form.getlist('Country'), \
        'MajorManufacturer': request.form.getlist('MajorManufacturer'), \
        'Designer': request.form.getlist('Designer'), \
        'MajorClassification': request.form.getlist('MajorClassification'), \
        'MajorCartridge': request.form.getlist('MajorCartridge'), \
        'FireSystem': request.form.getlist('FireSystem'), \
        'Action': request.form.getlist('Action'), \
        'Barrels': request.form.getlist('Barrels'), \
        'MandP_MajorPerpose_1': request.form.getlist('MandP_MajorPerpose'), \
        'MandP_MajorPerpose_2': request.form.getlist('MandP_MajorPerpose'), \
        'Traditional_tag_1': request.form.getlist('Traditional_tag'), \
        'Traditional_tag_2': request.form.getlist('Traditional_tag'), \
        'Traditional_tag_3': request.form.getlist('Traditional_tag'), \
        'Traditional_tag_4': request.form.getlist('Traditional_tag'), \
        'Traditional_tag_5': request.form.getlist('Traditional_tag'), \
        'FeedSystem_1': request.form.getlist('FeedSystem'), \
        'FeedSystem_2': request.form.getlist('FeedSystem'), \
        'TriggerSystem': request.form.getlist('TriggerSystem'), \
        'BoltStyle': request.form.getlist('BoltStyle')}

    if len(input_request_dict['Gun_MajorName']) == 0:
        input_request_dict['Gun_MajorName'] = ['']
    if len(input_request_dict['Gun_MajorName'][0]) != 0:
        input_request_dict['Gun_MajorName'][0] = unicodedata.normalize('NFKC', input_request_dict['Gun_MajorName'][0] + '%')

    print(input_request_dict['Gun_MajorName'], flush=True)
    return input_request_dict

# SQLの処理文を自動生成して実行
def create_sql(cur, input_request_dict):

    sql_sentence = \
        "SELECT * FROM Guns \
        LEFT JOIN Gun_Nicknames \
            ON Guns.ID = Gun_Nicknames.GunsID \
        LEFT JOIN Uncertain_elements \
            ON Guns.ID = Uncertain_elements.GunsID \
        WHERE \
            CASE \
                WHEN " + str(len(input_request_dict['Gun_MajorName'][0])) + " <> 0 \
                    THEN Gun_MajorName LIKE " + str(input_request_dict['Gun_MajorName']).replace('[', '(').replace(']', ')') + \
                    " OR  Nickname_1 LIKE " + str(input_request_dict['Gun_MajorName']).replace('[', '(').replace(']', ')') + \
                    " OR  Nickname_2 LIKE " + str(input_request_dict['Gun_MajorName']).replace('[', '(').replace(']', ')') + \
                " ELSE 1 = 1 \
            END \
        AND CASE \
            WHEN " + str(len(input_request_dict['Country'])) + " <> 0 \
                THEN Country IN " + str(input_request_dict['Country']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['MajorManufacturer'])) + " <> 0 \
                THEN MajorManufacturer IN " + str(input_request_dict['MajorManufacturer']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['Designer'])) + " <> 0 \
                THEN Designer IN " + str(input_request_dict['Designer']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['MajorClassification'])) + " <> 0 \
                THEN MajorClassification IN " + str(input_request_dict['MajorClassification']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['MajorCartridge'])) + " <> 0 \
                THEN MajorCartridge IN " + str(input_request_dict['MajorCartridge']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['FireSystem'])) + " <> 0 \
                THEN FireSystem IN " + str(input_request_dict['FireSystem']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['TriggerSystem'])) + " <> 0 \
                THEN TriggerSystem IN " + str(input_request_dict['TriggerSystem']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['Action'])) + " <> 0 \
                THEN Action IN " + str(input_request_dict['Action']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['Barrels'])) + " <> 0 \
                THEN Barrels IN " + str(input_request_dict['Barrels']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['MandP_MajorPerpose_1'])) + " <> 0 \
                THEN MandP_MajorPerpose_1 IN " + str(input_request_dict['MandP_MajorPerpose_1']).replace('[', '(').replace(']', ')') + \
                " OR MandP_MajorPerpose_2 IN " + str(input_request_dict['MandP_MajorPerpose_2']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['Traditional_tag_1'])) + " <> 0 \
                THEN Traditional_tag_1 IN " + str(input_request_dict['Traditional_tag_1']).replace('[', '(').replace(']', ')') + \
                " OR Traditional_tag_2 IN " + str(input_request_dict['Traditional_tag_2']).replace('[', '(').replace(']', ')') + \
                " OR Traditional_tag_3 IN " + str(input_request_dict['Traditional_tag_2']).replace('[', '(').replace(']', ')') + \
                " OR Traditional_tag_4 IN " + str(input_request_dict['Traditional_tag_2']).replace('[', '(').replace(']', ')') + \
                " OR Traditional_tag_5 IN " + str(input_request_dict['Traditional_tag_2']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['FeedSystem_1'])) + " <> 0 \
                THEN FeedSystem_1 IN " + str(input_request_dict['FeedSystem_1']).replace('[', '(').replace(']', ')') + \
                " OR FeedSystem_2 IN " + str(input_request_dict['FeedSystem_2']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['TriggerSystem'])) + " <> 0 \
                THEN TriggerSystem IN " + str(input_request_dict['TriggerSystem']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END \
        AND CASE \
            WHEN " + str(len(input_request_dict['BoltStyle'])) + " <> 0 \
                THEN BoltStyle IN " + str(input_request_dict['BoltStyle']).replace('[', '(').replace(']', ')') + \
            " ELSE 1 = 1 \
        END"

    print(sql_sentence.replace('\t', '').replace('\n', ''), flush = True)
    # SQL実行
    cur.execute(sql_sentence)
    all_data = cur.fetchall()
    return all_data

# データベースへ接続
def connect_db():
    # データベース接続
    db = sqlite3.connect("category_database/All_Gun_products.db")

    # データを辞書型に変換
    db.row_factory = dict_factory

    # 辞書型に変換しカーソルオブジェクトを作成
    cur = db.cursor()
    return db, cur

# データベース切断
def close_db(db):
    db.close()

# デフォルト: 全武器表示, ボタン発火で絞り込み
@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        # データベースに接続
        operate_db = connect_db()
        db_dict = match_DB2HTML(request)
        # SQL文を生成
        result_dict = create_sql(operate_db[1], db_dict)
        # close
        close_db(operate_db[0])

        result_len = len(result_dict)
        simple_list = ['Gun_MajorName', 'Country', 'brief_Comment']

        # フロント側と名前を揃える必要あり. 保存を忘れないように
        return render_template("index.html", gun_dict = result_dict, gun_len = result_len, simple_list = simple_list)
    else:
    #     cur.execute("SELECT * FROM Guns")
    #     all_data = cur.fetchall()
    #     # print(all_data, flush=True)
    #     db.close()
        return render_template("index.html")

# 武器選択時の動き
# ルーティングに変数を指定
@app.route('/result/<guns_id>', methods=['GET', 'POST'])
def result(guns_id):
    if request.method == 'GET':

        operate_db = connect_db()
        db_dict = match_DB2HTML(request)
        sql_sentence = \
            'SELECT * FROM Guns \
            LEFT JOIN Gun_Nicknames \
                ON Guns.ID = Gun_Nicknames.GunsID \
            LEFT JOIN Uncertain_elements \
                ON Guns.ID = Uncertain_elements.GunsID \
            WHERE Guns.ID = \"' + guns_id + '\"'
        operate_db[1].execute(sql_sentence)
        result_dict = operate_db[1].fetchall()
        close_db(operate_db[0])

        return render_template('result.html', result_dict = result_dict)
    else:
        return render_template('index.html')

#app.pyをターミナルから直接呼び出した時だけ、app.run()を実行する

# if __name__ == "__main__":
#     app.run(debug=True, host='0.0.0.0', port = 80)
if __name__ == "__main__":
    serve.run(debug= True, host= '0.0.0.0', port= 8000)

# sudo lsof -i :ポート番号
# sudo kill -9 PID