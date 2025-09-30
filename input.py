import keyboard
import time
import random
import os

QUESTION_NUM = 50                                               # 文章を入力する回数
input_data_all = []                                                 # 入力された全てのデータ
input_data = []                                                     # 入力されたデータ
chose_merosu_file = ''                                              # 選択されたローマ字タイプのメロス
rome_type = ''                                                      # 選択されたローマ字タイプ
text = []                                                           # 入力するテキスト(漢字、ひらがな、ローマ字の順)
text_lst = []                                                       # 実際に使用したテキスト群
save_file_timestamp = str(time.time())                              # 保存するファイルに使用するタイムスタンプ
save_file = './datas/input_' + save_file_timestamp + '.csv'         # 入力情報を保存
save_file_all = './datas/all_' + save_file_timestamp + '.csv'       # すべての入力情報を保存
save_file_text = './datas/text_' + save_file_timestamp + '.csv'     # 使用したテキストを保存する
text_list = []                                                      # 出題された問題のリスト

# 入力指示を表示する関数
def display_guide(QUESTION_NUM, question_cnt, text_cnt, text_num):
  os.system('cls')
  print(text_num)
  print(f"[{ question_cnt }/{ QUESTION_NUM }] 表示された文字を入力してください。")
  print(f"　入力　： { text[text_num]['kanji'] }")
  print(f"　かな　： { text[text_num]['kana'] }")
  print(f"ローマ字： { text[text_num]['rome'] }")
  print("　　　　　 " + ( "-" * text_cnt ))

# まず、ローマ字タイプを選択する
os.system('cls')
while True:
  print("ローマ字タイプを選択してください。aかbを入力後にEnterを押すことで進めます。\n")
  print("a: し=>shi, ち=>chi, つ=>tsu, ふ=>fu, じ=>ji, じゃ=>ja")
  print("b: し=>si,  ち=>ti,  つ=>tu,  ふ=>hu, じ=>zi, じゃ=>zya\n")
  rome_type = input("a or b: ")
  if rome_type == 'a':
    chose_merosu_file = 'merosu_short_rome_a.csv'
    break
  elif rome_type == 'b':
    chose_merosu_file = 'merosu_short_rome_b.csv'
    break
  else:
    os.system('cls')
    print("------------------------------")
    print("| ! aかbを入力してください ! |")
    print("------------------------------")
    
# メロスデータを読み込み
with open('merosu_short.csv', mode='r', encoding='utf-8') as f:
  with open('merosu_short_kana.csv', mode='r', encoding='utf-8') as kf:
    with open(chose_merosu_file, mode='r', encoding='utf-8') as rf:
      while True:
        kanji = f.readline()
        kana = kf.readline()
        rome = rf.readline()
        if kanji == '':
          break
        text.append({
          'kanji': kanji.replace('\n', ''),
          'kana': kana.replace('\n', ''),
          'rome': rome.replace('\n', '').replace(' ', '')
        })

# 入力処理
question_cnt = 1                        # 現在の問題番号
text_cnt = 0                            # 入力文字数
text_num = [266, 162, 56, 181, 100, 47, 240, 268, 99, 19, 170, 275, 178, 98, 90, 26, 106, 167, 142, 22, 236, 201, 120, 85, 221, 94, 27, 251, 86, 107, 278, 280, 198, 96, 214, 272, 211, 31, 282, 241, 14, 12, 218, 242, 281, 115, 83, 92, 18, 112]
display_guide(QUESTION_NUM, question_cnt, text_cnt, 266)
text_lst.append(text[266]['kanji'])
while True:
  input_key = keyboard.read_key()
  input_data_all.append({'key':input_key, 'timestamp':time.time()})
  if input_key != "":
    # 途中脱出
    if input_key == 'esc':
      break

    # 正しい入力だった場合、結果を保存
    # print(input_key, text[text_num[question_cnt-1]]['rome'][text_cnt])
    if input_key == text[text_num[question_cnt-1]]['rome'][text_cnt]:
      text_cnt += 1
      display_guide(QUESTION_NUM, question_cnt, text_cnt, text_num[question_cnt-1])
      input_data.append({'key':input_key, 'timestamp':time.time()})

      if text_cnt >= len(text[text_num[question_cnt-1]]['rome']):
        if question_cnt == QUESTION_NUM:
          # 事前に登録された回数の文章を入力し終わった場合、ループを抜けて結果を表示する
          break
        else:
          # 事前に登録された回数の文章を入力し終わっていな場合、新しい文章を表示する
          question_cnt += 1
          text_cnt = 0
          input_data.append({'key': 'change', 'timestamp':time.time()})  # 文章が変わるタイミング
          display_guide(QUESTION_NUM, question_cnt, text_cnt, text_num[question_cnt-1])
          text_lst.append(text[text_num[question_cnt-1]]['kanji'])

# 使用したテキスト群を保存
with open(save_file_text, mode='w', encoding='utf-8') as f:
  for text in text_lst:
    f.write(text + "\n")

# 入力した全てのキー情報を保存
with open(save_file_all, mode='w', encoding='utf-8') as f:
  for i in range(len(input_data_all)):
    f.write(f"{input_data_all[i]['key']},{input_data_all[i]['timestamp']}\n")

# 結果を保存
before_timestamp = 0.0
text = ""
with open(save_file, mode='w', encoding='utf-8') as f:
  for i, data in enumerate(input_data):
    # コンソールに表示
    current_key = data['key']
    timestamp = data['timestamp']
    # print(f"{current_key}, {timestamp-before_timestamp}")
    before_timestamp = timestamp
    text += current_key

    # ファイルに保存
    f.write(f"{current_key},{timestamp}\n")

os.system('cls')
print("./datasディレクトリに生成されたファイルをSlackで \"野中航希\" に送信してください。")
print("ご協力ありがとうございました！")