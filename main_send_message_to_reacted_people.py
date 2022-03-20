# リアクションした人たちにメッセージを送る
import sys
import importlib
import facebook_scraper
#importlib.reload(facebook_scraper)
from facebook_scraper import FacebookScraper

def main():
    if len(sys.argv) < 4:
        print('引数が足りません。以下の値を実行時に引数として入力してください。')
        print('[1] : 一番新しい投稿から数えたとき、何番目の投稿を対象とするのか')
        print('[2] : 対象とする投稿をした人の FaceBook のトップページ')
        print('[3] : ログインに使うパスワード')
        print('[4] : ログインに使うメールアドレスまたは電話番号')
        return

    index_of_post       = int(sys.argv[1]) - 1
    target_top_page_url = sys.argv[2]
    password            = sys.argv[3]
    email_or_number     = sys.argv[4]

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
        email_or_number,
        password,
        False,
    )
    # リアクションした人たちの URL を取得
    urls_of_reacted_people = scraper.get_urls_of_reacted_people(target_top_page_url, index_of_post)
    # メッセージの送信
    size = len(urls_of_reacted_people)
    for i, url in enumerate(urls_of_reacted_people):
        print(f'{i} / {size}   url = {url}')
        scraper.send_message(url, text_for_send)


if __name__ == '__main__':
    main()
