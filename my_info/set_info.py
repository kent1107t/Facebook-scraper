import json
from os import path
from pprint import pprint


info_fpath = './info.json'

info_dict = {}
print('今の値')
# 今の info.json を辞書として読み込み
if path.exists(info_fpath):
    with open(info_fpath) as f:  info_dict = json.load(f)
pprint(info_dict, width=40)

info_dict  = {}
# 値の設定
info_dict['my_email_or_number']  = input('\nログインに使うメールアドレスもしくは電話番号を入力してください。\n')
info_dict['my_password']         = input('\nログインに使うパスワードを入力してください。\n')
info_dict['target_top_page_url'] = input('\n対象となる投稿をする人の Facebook のトップページの URL を入力してください。\n')


print('\n新しい値')
pprint(info_dict, width=40)
# 辞書の書き込み
with open(info_fpath, 'w') as f:
    json.dump(info_dict, f, indent=4, ensure_ascii=False)
