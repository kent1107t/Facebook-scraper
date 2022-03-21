# リアクションした人たちにメッセージを送る
import sys
import json
from pprint import pprint
from facebook_scraper import FacebookScraper

def main():
    # ログインのための情報などを保存したファイルから読み込み
    with open('my_info/info.json') as f:  info_dict = json.load(f)
    my_email_or_number  = info_dict['my_email_or_number']
    my_password         = info_dict['my_password']
    target_top_page_url = info_dict['target_top_page_url']

    # 今回のターゲットとなる投稿の情報を入力
    target_top_page_url = input('対象とする投稿をした人の FaceBook のトップページを入力してください : ')
    index_of_post = int(input('一番新しい投稿から数えたとき、何番目の投稿を対象とするのかを入力してください : '))
    index_of_post -= 1  # 0-indexed に

    # メッセージの入力
    text_for_send = ''
    print('送るメッセージの本文を入力してください。入力が終わりましたら、コントロールキーと"C"を押してください。\n\n')
    while True:
        if text_for_send != '':  text_for_send += '\n'
        try:
            text_for_send += input()
        except:
            break
    print('\n'+text_for_send)

    # ログインとか
    scraper = FacebookScraper(
        my_email_or_number,
        my_password,
        False,
    )
    
    # リアクションした人たちの URL を取得
    urls_of_reacted_people = scraper.get_urls_of_reacted_people(target_top_page_url, index_of_post)
    # メッセージの送信
    size = len(urls_of_reacted_people)
    for i, url in enumerate(urls_of_reacted_people, start=1):
        print(f'{i:3}人目 / 全{size:3}人   url = {url}')
        scraper.send_message(url, text_for_send)


if __name__ == '__main__':
    main()
