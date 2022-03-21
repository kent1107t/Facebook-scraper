# リアクションした人たちにメッセージを送る
import sys
import json
from os import path
from pprint import pprint
from facebook_scraper import FacebookScraper


def send_message_to_reacted_people(
        scraper: FacebookScraper,   # ログイン済みscraper
        target_top_page_url: str,   # 対象の投稿があるトップページ
        indexes_of_post: [int],     # 対象の投稿の番号
        text_of_message: str,       # メッセージとして送る本文
) -> None:
    # リアクションした人たちの URL を取得  {index_of_post: [url]} の形
    urls_of_reacted_people_per_post = scraper.get_urls_of_reacted_people_per_post(target_top_page_url, indexes_of_post)

    # メッセージの送信
    for index_of_post, urls in urls_of_reacted_people_per_post.items():
        print(f'投稿 {index_of_post+1} について')
        number_of_reacted_people = len(urls)
        for i, url in enumerate(urls, start=1):
            print(f'{i:2} / {number_of_reacted_people:2}  人目の人にメッセージを送っています...')
            scraper.send_message(url, text_of_message)


def main():
    # ログインのための情報などを保存したファイルから読み込み
    my_info_fpath = path.join(path.dirname(path.abspath(__file__)), 'my_info', 'info.json')
    with open(my_info_fpath) as f:  my_info_dict = json.load(f)
    my_email_or_number  = my_info_dict['my_email_or_number']
    my_password         = my_info_dict['my_password']
    target_top_page_url = my_info_dict['target_top_page_url']

    # 送るメッセージの読み込み
    text_of_message_fpath = path.join(path.dirname(path.abspath(__file__)), 'text_of_message.txt')
    text_of_message = ''
    with open(text_of_message_fpath) as f:  text_of_message = f.read()
    if 'y' != input(f'{"-"*44}\n{text_of_message}\n{"-"*44}\n\n以上の内容でメッセージを送ります。よろしいですか？\nよろしい場合は "y" を、やり直す場合はそれ以外の文字を入力してください。 : '):
        print('プログラムを終了します。')
        return

    # 今回のターゲットとなる投稿の情報を入力 (入力は 1-indexed)
    *indexes_of_post, = map(lambda idx: int(idx)-1, input('一番新しい投稿から数えたとき、何番目の投稿を対象とするのかを、"空白区切り" で、入力してください。\n').split())

    # ログインとか
    scraper = FacebookScraper(
        my_email_or_number,
        my_password,
        False,
    )
    
    # メッセージの送信
    send_message_to_reacted_people(
        scraper,
        input('target ?   :  '), #target_top_page_url,
        indexes_of_post,
        text_of_message,
    )

if __name__ == '__main__':
    main()
