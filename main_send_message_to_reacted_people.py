# リアクションした人たちにメッセージを送る

from facebook_scraper import FacebookScraper

def main():
    if len(sys.argv) != 5:
        print('引数が足りません。以下の値を実行時に引数として入力してください。')
        print('[1] : ログインに使うメールアドレスまたは電話番号')
        print('[2] : ログインに使うパスワード')
        print('[3] : 対象とする FaceBook のページ')
        print('[5] : 結果を保存するファイルのパス')
        return

    email_or_number     = sys.argv[1]
    password            = sys.argv[2]
    target_top_page_url = sys.argv[3]

    scraper = FacebookScraper(
        email_or_number,
        password,
        False,
    )

    scraper.send_message_by_messenger_to(names)

    scraper.get_urls_of_reacted_people_per_posts(target_top_page_url, 

if __name__ == '__main__':
    main()
