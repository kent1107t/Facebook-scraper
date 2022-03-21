# リアクションした人たちにメッセージを送る
import sys
import json
from os import path
from pprint import pprint
from facebook_scraper import FacebookScraper


def get_info_dict_of_reacted_people_per_post(
        scraper: FacebookScraper,   # ログイン済みscraper
        target_top_page_url: str,   # 対象の投稿があるトップページ
        indexes_of_post: [int],     # 対象の投稿の番号
) -> {int: {str: {}}}:  # {index_of_post: {url: {urlの人の各情報の辞書}}}
    # リアクションした人たちの URL を取得  {index_of_post: [url]} の形
    urls_of_reacted_people_per_post = scraper.get_urls_of_reacted_people_per_post(target_top_page_url, indexes_of_post)
    # 取得した人たちに対して、ページから情報を取得
    return {index: {url: scraper.get_info_dict_by_top_page_url(url) for url in urls} for index, urls in urls_of_reacted_people_per_post.items()}


def write_info_dicts_on_xl(
        info_dict_of_reacted_people_per_post: {int: {str: {}}},
        xl_file_path: str
) -> None:
    # xl_file_path のエクセルファイルに、リアクションした人たちの情報を書き込む
    import openpyxl
    # ブック・シートを取得
    wb = openpyxl.load_workbook(xl_file_path)
    sheet = wb['Sheet1']
    # scraper.KEYS_OF_INFO_DICT にキー集合が入ってる
    # 表示順で並べたキー集合
    keynames_on_display_order = [
        'URL',
        '名前',
        '在住',
        '勤務先',
        '電話番号',
        '出身地',
        '出身校',
        '交際',
    ]
    # 項目のキーから、その情報を表示する列のインデックス
    keyname2column = {keyname: i for i, keyname in enumerate(keynames_on_display_order, start=1)}
    # 今の書き込む行を持つ変数
    row4write = 1
    # 各投稿ごとに
    for index_of_post, info_dict_of_reacted_people in info_dict_of_reacted_people_per_post.items():
        # 各人ごとに
        for url, info_dict in info_dict_of_reacted_people.items():
            # 各情報の項目ごとに
            for info_key, info_value in info_dict.items():
                sheet.cell(row=row4write, column=keyname2column[info_key], value=info_value)
            row4write += 1
        # 投稿ごとに空行を挟む
        row4write += 1

    wb.save(xl_file_path)
    print('エクセルファイルに結果を出力しました。')


def main():

    # ログインのための情報などを保存したファイルから読み込み
    my_info_fpath = path.join(path.dirname(path.abspath(__file__)), 'my_info', 'info.json')
    with open(my_info_fpath) as f:  my_info_dict = json.load(f)
    my_email_or_number  = my_info_dict['my_email_or_number']
    my_password         = my_info_dict['my_password']
    target_top_page_url = my_info_dict['target_top_page_url']

    # 今回のターゲットとなる投稿の情報を入力 (入力は 1-indexed)
    *indexes_of_post, = map(lambda idx: int(idx)-1, input('一番新しい投稿から数えたとき、何番目の投稿を対象とするのかを、"空白区切り" で、入力してください。\n').split())

    # 保存するエクセルのパス
    xl_file_path = path.join(path.dirname(path.abspath(__file__)), 'info_of_reacted_people.xlsx')
    if not path.exists(xl_file_path):
        if 'y' != input(f'パス {xl_file_path} は存在しません。結果はエクセルファイルに保存されませんがよろしいですか？\nよろしい場合は "y" を、やり直す場合はそれ以外の文字を入力してください。 : '):
            print('プログラムを終了します。')
            return

    # ログインとか
    scraper = FacebookScraper(
        my_email_or_number,
        my_password,
        False,
    )

    # 取得した人たちに対して、ページから情報を取得
    info_dict_of_reacted_people_per_post = get_info_dict_of_reacted_people_per_post(scraper, target_top_page_url, indexes_of_post)

    # エクセルに保存しない場合は表示して終わる
    if not path.exists(xl_file_path):
        pprint(info_dict_of_reacted_people_per_post)
        return

    # 結果をエクセルファイルに保存
    write_info_dicts_on_xl(info_dicts_of_reacted_people_per_post, xl_file_path)


if __name__ == '__main__':
    main()
