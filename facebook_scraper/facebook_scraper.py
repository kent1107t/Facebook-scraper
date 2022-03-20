'''
環境構築などの参考
https://qiita.com/Chanmoro/items/9a3c86bb465c1cce738a
https://stackoverflow-com.translate.goog/questions/56155627/requestsdependencywarning-urllib3-1-25-2-or-chardet-3-0-4-doesnt-match-a-s?_x_tr_sl=en&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_pto=sc
webelement の参考
https://developer.mozilla.org/ja/docs/Web/API/HTMLAnchorElement/href
https://kurozumi.github.io/selenium-python/api.html#selenium.webdriver.remote.webelement.WebElement
https://www.seleniumqref.com/api/python/element_infoget/Python_get_attribute.html
https://developer.mozilla.org/ja/docs/Web/API/Element/scroll
https://qiita.com/maruo327/items/36be1a34b88e389bc2b0
https://kurozumi.github.io/selenium-python/api.html
https://stackoverflow-com.translate.goog/questions/69095078/how-to-disable-drag-of-a-element-when-dragging-a-horizontal-scrollbar?_x_tr_sl=en&_x_tr_tl=ja&_x_tr_hl=ja&_x_tr_pto=sc
https://www.selenium.dev/ja/documentation/webdriver/elements/finders/
https://office54.net/python/scraping/selenium-element-iframe
'''
import sys
import doctest
import json
import os
import re
from time import sleep, perf_counter
import chromedriver_binary
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


class ClassNames:
    # 取得したいクラス名をまとめたクラス 
    # 空白区切りでクラス名を指定してる要素（複数のクラス指定）は、クラス名からではなくcss-selectorから、値の指定は .name1.name2.name3...nameX の形式でする
    # 参考  https:/p/note.com/scrayper_1/n/ncc2abf930fd7

    # 各投稿に設定されているクラス名 投稿数を数えるのに使ってる
    POSTS = 'du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'
    # リアクションした人たちを表示するボタンに使われてるクラス名
    BUTTON_DISPLAY_REACTED_PEOPLE = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of n00je7tq arfg74bv qs9ysxi8 k77z8yql l9j0dhe7 abiwlrkh p8dawk7l lzcic4wl gmql0nx0 ce9h75a5 ni8dbmo4 stjgntxs a8c37x1j'
    # リアクションした人たちを表示するボタン要素の中の、人数の値が入ってる要素のクラス名
    HAS_NUMBER_IN_BUTTON_DISPLAY = 'gpro0wi8 pcp91wgn'

    # 一覧表示ページ
    # 一覧の表示を閉じるボタン
    CLOSE_BUTTON_ON_DISPLAYED_PAGE = 'oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn s45kfl79 emlxlaya bkmhp75w spb7xbtv rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv j83agx80 taijpn5t jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 tv7at329 thwo4zme tdjehn4e'
    # 一覧表示ページの、スクロールバーの役割をしてる要素のクラス名
    SCROLL_VAR_ON_DISPLAYED_PAGE = 'oj68ptkr jk6sbkaj kdgqqoy6 ihh4hy1g qttc61fc datstx6m k4urcfbm'
    # リアクションした人たちのリストが入ってる、最小の共通要素のとこのクラス名
    GROUP_OF_DISPLAY_LIST = 'rpm2j7zs k7i0oixp gvuykj2m j83agx80 cbu4d94t ni8dbmo4 du4w35lb q5bimw55 ofs802cu pohlnb88 dkue75c7 mb9wzai9 l56l04vs r57mb794 l9j0dhe7 kh7kg01d eg9m0zos c3g1iek1 otl40fxz cxgpxx05 rz4wbd8a sj5x9vvc a8nywdso'
    # 一覧表示ページの、それぞれの人へのリンクが入ってるクラスの名前 このままだとたぶんほかのリンク（広告ページとか）も混ざってるから、ソースの中で特定の領域とかで判別する必要あri
    LINK_TO_REACTED_PERSON = 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p'

    # その人のページで、ビジネスアカウントかどうかを判別する要素のクラス名
    FRIEND_OR_GOOD_BUTTON = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v lrazzd5p a57itxjd'

    # プロフィールページの、その人の名前が入ってるクラス名
    FULL_NAME = 'gmql0nx0 l94mrbxd p1ri9a11 lzcic4wl'
    # プロフィールページの、各情報のリストのグループのクラス名
    #GROUP_OF_ABOUT = 'buofh1pr'  グループの一番上のクラス名
    GROUP_OF_ABOUT = 'dati1w0a tu1s4ah4 f7vcsfb0 discj3wi'  # グループの上から二番目のクラス名
    # プロフィールページの、各情報のリストのクラス名 左にあるアイコンの情報で何のキー（居住地とか出身大学とか）かを認識する必要があるから、そこまでを含めたクラス名
    ITEM_OF_ABOUT = "rq0escxv l9j0dhe7 du4w35lb j83agx80 pfnyh3mw jifvfom9 gs1a9yip owycx6da btwxx1t3 jb3vyjys b5q2rw42 lq239pai mysgfdmx hddg9phg"
    # プロフィールページの、各情報のリストの本文のクラス名
    VALUE_OF_ITEM_OF_ABOUT = 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d9wwppkn hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id'
    # プロフィールページの、各情報のリストのサブの説明的なとこのクラス名
    SUB_VALUE_OF_ITEM_OF_ABOUT = 'j5wam9gi e9vueds3 m9osqain'

    # Messenger のボタン
    MESSENGER_BUTTON = 'oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn s45kfl79 emlxlaya bkmhp75w spb7xbtv rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv j83agx80 taijpn5t jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 qypqp5cg q676j6op tdjehn4e'



class FacebookScraper:
    FACEBOOK_TOP_URL = r'https://www.facebook.com/'
    classnames = ClassNames()

    def __init__(
            self, 
            my_email_or_number: str,
            my_password: str,
            is_mode_headless=False
    ):
        self.is_mode_headless = is_mode_headless

        self.options = self.__get_options()
        self.driver = self.__get_driver()
        # リアクションした人たちを見るにはログインが必要
        self.login_to_facebook_top_page(my_email_or_number, my_password)
        # get_info_dict_of_reacted_people で帰る辞書のキー集合
        self.KEYS_OF_INFO_DICT = set()
        # 人の URL から、名前を取得する辞書 リアクションした人の取得時に蓄積してく
        self.url2fullname = {}

    def __del__(self):
        self.driver.quit()

    def send_message_by_messenger_to(
            self,
            names: [str]           # メッセージを送る人のリスト
    ) -> None:
        '''
        引数でもらった人の名前のリストに対してメッセージを送る
        '''
        self.driver.get('https://www.facebook.com/messages/new')
        # 宛先に入れるのに失敗した名前 最後に表示する
        names_of_failed = []
        for name in names:
            # 宛先名を入れるテキストボックスの要素
            dear_input_elem = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+'g5ia77u1 gcieejh5 bn081pho humdl8nn izx4hr6d rq0escxv oo9gr5id nc684nl6 jagab5yi knj5qynh fo6rh5oj aov4n071 oi9244e8 bi6gxh9e h676nmdw d2edcug0 lzcic4wl ieid39z1 osnr6wyh aj8hi1zk kd8v7px7 r4fl40cc m07ooulj mzan44vs'.replace(' ', '.'))
            dear_input_elem.send_keys(name)
            sleep(0.4)
            # 宛先に入ってる文字列からサジェストされた人の要素
            try:
                suggest_elem = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+"rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t d2edcug0 hpfvmrgz rj1gh0hx buofh1pr g5gj957u p8fzw8mz pcp91wgn iuny7tx3 ipjc6fyt".replace(' ', '.'))
            except:
                # サジェストが無い場合
                dear_input_elem.clear()
                names_of_failed.append(name)
            else:
                suggest_elem.click()
            sleep(0.4)
        print('以下の名前の人たちを宛先に入れることに失敗しました。手動で入れてください')
        # リアクションした人たちならこの辞書にURLと名前が紐づけてあるので、そのURLも表示しておく
        name2url = {name: url for url, name in self.url2fullname.items()}
        for name_of_failed in names_of_failed:
            url_of_name = '不明'
            if name_of_failed in name2url:  url_of_name = name2url[name_of_failed]
            print(f'    {name_of_failed}  (URL : {url_of_name})')
        input('\nメッセージの本文や添付を埋め、送信してください。\n送信後、もしくは送信せずにプログラムを終了する場合には、このままエンターキーを押してください。')
        return


    def get_urls_of_reacted_people(
            self,
            target_top_page_url: str,       # 対象とする人のページ
            index_of_post: int,             # 対象とする投稿の、一番新しい投稿から見たときの番号 (0-indexed)
            need_confirm: bool = False,     # 投稿の文字を表示して、対象の投稿かを確認する
    ) -> [str]:
        while True:
            # 投稿とボタンの要素を必要な分取得
            self.__set_post_and_button_elems(target_top_page_url, index_of_post + 1)
            # 確認する必要がなければそのまま出る
            if not need_confirm:  break
            # 入力し直す必要があるか確認し、必要がなければそのまま出る
            print('-'*55, *list(map(lambda s: '    '+s, self.post_elems[index_of_post].text.split('\n')[:5])), '-'*55, sep='\n')
            need_redo = ('y' != input('対象とする投稿は以上のものでよろしいでしょうか？\nよろしい場合は "y" を入力しエンターキーを押してください  :  '))
            if not need_redo:  break
            # 新しい投稿の番号を入力
            while True:
                index_of_post = input('    一番新しい投稿から数えたとき、対象とする投稿が何番目かを入力してエンターキーを押してください。  :  ')
                if not index_of_post.isdecimal() or int(index_of_post) <= 0:
                    print('        正の数字を入力してください。')
                    continue
                index_of_post = int(index_of_post) - 1
                break
        # リアクションした人たちを表示するボタンを持っていない --> リアクションした人の数が 0 なので空のリストを返す
        if not index_of_post in self.post_index2button_index:  return []
        # 人の一覧を表示するボタン要素から、その一覧の人たちのトップページの URL を取得する
        urls = self.__get_urls_of_reacted_people_from_button_elem(self.button_elems[self.post_index2button_index[index_of_post]])
        self.__print_done_message_with_sleep(0.1)
        return urls

    def get_urls_of_reacted_people_per_posts(
            self,
            target_top_page_url: str,       # 対象とする人のページ
            number_of_target_posts: int,  # 対象とする投稿の数
    ) -> [[str]]:
        '''
        各投稿について、リアクションした人の URL を返す関数
        '''
        # 投稿とボタンの要素を必要な分取得
        self.__set_post_and_button_elems(target_top_page_url, number_of_target_posts)
        # 各投稿要素について、ボタン要素を取得し（存在すれば リアクションした人数が0なら存在しない）、ボタン要素からリアクションした人たちの URL を取得する
        urls_per_posts = [[] for _ in range(number_of_target_posts)]  # 投稿の数 x リアクションした人の数 の二次元リスト
        print('各投稿について、リアクションした人達の FACEBOOK ページの URL を取得しています ... ')
        for i, post_elem in enumerate(self.post_elems):
            print(f'    投稿 {i+1:3} / {len(post_elems):3} について')
            urls_per_posts[i] = []
            # リアクションした人の数が 0 なら、ボタン要素も無いのでスキップ
            if not self.__does_post_have_button_display_reacted_people(post_elem):
                print('        リアクションした人の数は 0 です')
                continue
            button_elem = self.button_elems[self.post_index2button_index[i]]
            # 人の一覧を表示するボタン要素から、その一覧の人たちのトップページの URL を取得する
            urls_per_posts[i] = self.__get_urls_of_reacted_people_from_button_elem_display(button_elem, current_button_index)
            current_button_index += 1
        self.__print_done_message_with_sleep(0.1)
        return urls_per_posts

    def __does_post_have_button_display_reacted_people(self, post_elem):
        # もらった投稿の要素 post_elem の中にリアクションした人を表示するボタン要素があるかどうかを返す
        return  post_elem.get_attribute("innerHTML").count(self.classnames.BUTTON_DISPLAY_REACTED_PEOPLE) > 0

    def get_info_dicts_of_reacted_people_per_posts(
            self,
            target_top_page_url: str,       # 対象とする人のページ
            number_of_target_posts: int,  # 対象とする投稿の数
    ) -> [{}]:
        '''
        引数の人の投稿にリアクションした人の情報の dict を、各投稿の分だけリストにして返す
        len(返り値)         -->   対象とする投稿の数 (number_of_target_posts)
        返り値[i].keys()    -->   i 番目投稿にリアクションした人たちの URL の集合
        返り値[i].values()  -->   i 番目投稿にリアクションした人たちの情報(dict)の集合
        '''
        # 対象の投稿数までのすべての投稿について、リアクションした人たちの URL を取得
        urls_of_reacted_people_per_posts = self.get_urls_of_reacted_people_per_posts(target_top_page_url, number_of_target_posts)
        #print('TOUR in top page urls of reacted people')
        print('リアクションした人たちのページから情報を取得します ... ')
        info_dicts_per_posts = [{} for _ in range(number_of_target_posts)]  # 投稿の数だけ、URL をキーとしたその人の情報の辞書を返す
        for i, top_page_urls in enumerate(urls_of_reacted_people_per_posts):
            print(f'    投稿 {i+1:3} / {number_of_target_posts:3} について')
            for j, top_page_url in enumerate(top_page_urls):
                print(f'        URL {j+1:3} / {len(top_page_urls):3}  {top_page_url}')
                info_dicts_per_posts[i][top_page_url] = self.get_info_dict_by_top_page_url(top_page_url)
        return info_dicts_per_posts


    def get_info_dict_by_top_page_url(
            self,
            top_page_url: str
    ) -> {}:
        '''
        対象とする人のトップページの URL を引数に、そこからプロフィールページに移動し基本情報を辞書にまとめ返す
        '''
        # キー名を特定するために、左にあるアイコンのリンクをマークとして使ってる
        aboutthing2mark2keyname = {
            'overview': {  # 概要
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yt/r/Bo7x4xsiTje.png"' : '勤務先',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yN/r/j-QTXcNyQBK.png"' : '出身校',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yS/r/poZ_P5BwYaV.png"' : '在住',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yI/r/JbJK4O72TNa.png"' : '出身地',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yL/r/JS_uliVTrzJ.png"' : '交際',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yg/r/qm5n1WSqkVV.png"' : '交際',
                'src="https://static.xx.fbcdn.net/rsrc.php/v3/yI/r/lzvufuLgbzd.png"' : '電話番号',
            },
        }
        '''
        とりあえず概要のとこ以外はまだいいや
            'work_and_education': {  # 職歴と学歴
            },       
            'places': {  # 住んだことがある場所
            },
            'contact_and_basic_info': {  # 連絡先と基本データ
            },
            'family_and_relationships': {  # 家族と交際ステータス
            },
            'details': {  # 〜さんの情報
            },
            'life_events': {  # ライフイベント
            },
        }
        '''
        # 基本データのページを取得
        profile_page_url = self.get_profile_page_url_from_top_page_url(top_page_url)
        self.driver.get(profile_page_url)
        # 返り値の辞書 最初に名前と URL を入れとく
        info_dict = {
            '名前': self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.FULL_NAME.replace(' ', '.')).text,
            'URL' : top_page_url,
        }
        self.KEYS_OF_INFO_DICT = set()
        self.KEYS_OF_INFO_DICT |= set(info_dict.keys())
        self.KEYS_OF_INFO_DICT |= {keyname for mark2keyname in aboutthing2mark2keyname.values() for keyname in mark2keyname.values()}
        # デフォルトで空文字を入れとく キーをすべてのページで統一するため
        for keyname in self.KEYS_OF_INFO_DICT:
            if not keyname in info_dict:  info_dict[keyname] = ''
        # それぞれの項目についてまわっていく
        for about_thing, mark2keyname in aboutthing2mark2keyname.items():
            self.driver.get(f'{profile_page_url}_{about_thing}')
            # 項目が所属してる上のクラスの要素を取得 一応項目から直接取るんじゃなくて、一回グループとして取る
            sleep(0.4)
            try:
                group_elem = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.GROUP_OF_ABOUT.replace(' ', '.'))
            except:
                return info_dict  # ビジネスアカウントの場合
            # 各項目の要素を取得（住んだことがある場所 だと、居住地・出身地 とか）
            item_elems = group_elem.find_elements(by=By.CSS_SELECTOR, value='.'+self.classnames.ITEM_OF_ABOUT.replace(' ', '.'))
            # マークが存在してるかでそのキー名を特定 & description要素等を取得する時にソースの確認用
            innerHTMLs_of_item = [item_elem.get_attribute('innerHTML') for item_elem in item_elems]
            for i, (item_elem, innerHTML) in enumerate(zip(item_elems, innerHTMLs_of_item)):
                # read_value は value が優先 もし無い場合に sub_value なので、sub_value を先に入れようとしてる
                keyname, read_value = self.__get_keyname_by_innerHTML(innerHTML, mark2keyname), ''
                # 項目によって要素がそもそも存在しない場合が多々あるので、ソースをいちいち確認する
                if self.classnames.SUB_VALUE_OF_ITEM_OF_ABOUT in innerHTML:  # 説明書きみたいなの 項目がありませんとか 今の職業に対しての以前の職業とか
                    sub_value_elem = item_elem.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.SUB_VALUE_OF_ITEM_OF_ABOUT.replace(' ', '.'))
                    read_value = sub_value_elem.text
                if self.classnames.VALUE_OF_ITEM_OF_ABOUT in innerHTML:      # 今の値
                    value_elem = item_elem.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.VALUE_OF_ITEM_OF_ABOUT.replace(' ', '.'))
                    read_value = value_elem.text
                info_dict[keyname] = read_value
                print(f'        info_dict[{keyname}] = {info_dict[keyname]}')
        return info_dict
    
    
    @staticmethod
    def __get_keyname_by_innerHTML(innerHTML: str, mark2keyname: {}, unknown_keyname='unknown') -> str:
        # 項目の innerHTML を使って、マークとして登録してある左のアイコンのクラス名から、キーの名前（項目の名前）をげっとする
        for mark, keyname in mark2keyname.items():
            if mark in innerHTML:
                return keyname
        return unknown_keyname
    

    def __get_top_page_urls_of_reacted_people_on_displayed_page(self) -> [str]:
        '''
        リアクションした人たちの一覧が載ってるページにいる前提で、それぞれの人のトップページの URL を取得してリストで返す
        '''
        # 人の一覧が載ってるとこの共通クラスを取得
        group_elem_display_list = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.GROUP_OF_DISPLAY_LIST.replace(' ', '.'))
        # リアクションした人たちのリンクが入ってるグループの要素の中から、リンクの要素を取得する
        link_elems = group_elem_display_list.find_elements(by=By.CSS_SELECTOR, value='.'+self.classnames.LINK_TO_REACTED_PERSON.replace(' ', '.'))
        # リンクの要素から href の値をげっと
        urls = [e.get_attribute('href') for e in link_elems]
        # 必要な部分以外のクエリパラメータを消す
        urls = [self.__get_abs_top_page_url(url) for url in urls]
        # 後でいちいちurlに移動して名前を取得しないで済むようにここでセットしとく
        for link_elem, abs_url in zip(link_elems, urls):  self.url2fullname[abs_url] = link_elem.text
        return urls

    def __load_page_display_reacted_people_until_get_urls(
            self, 
            number_of_reacted_people: int,  # 一覧に表示されるべき人の数
    ) -> None:
        '''
        ちゃんんともらった値の数だけ一覧が表示されるまで、ページを読み込んでいく関数
        （追記）値の数と一致するとは限らないみたい だから、ある程度停滞が続いても終了することにした
        '''
        var_elem = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.SCROLL_VAR_ON_DISPLAYED_PAGE.replace(' ', '.'))
        prv_count_reacted_people, cur_count_reacted_people = -1, 0
        stagnation_count = 0  # 何回停滞が続いてるかを持つ変数

        for scroll_count in range(10000):
            # ここの値は読み込むごとにバーの大きさが小さくなっていって、下まで行ける値が大きくなっていくぽいから、毎回煮豚んでしてる
            dh_ok, dh_no = 0, 800
            while dh_ok + 3 < dh_no:
                sleep(0.3)
                dh_mid = (dh_ok + dh_no) // 2
                #print(f'ok : {dh_ok}   mid : {dh_mid}   no : {dh_no}')
                try:  ActionChains(self.driver).drag_and_drop_by_offset(var_elem, 0, dh_mid).perform()
                except Exception as e:  dh_no = dh_mid
                else:    dh_ok = dh_mid
            sleep(0.6)
	    # 今読み込めてるリアクションした人のページのURLリストを取得し、その数を更新
            cur_count_reacted_people = len(self.__get_top_page_urls_of_reacted_people_on_displayed_page())
            if cur_count_reacted_people > prv_count_reacted_people:
                print(f'         （読み込み中） 現在取得されている人数 : {cur_count_reacted_people} / {number_of_reacted_people}')
                prv_count_reacted_people = cur_count_reacted_people
                stagnation_count = 0
            else:
                stagnation_count += 1
            # ソースコードから取得した人数とイコールになれば終了 
            if cur_count_reacted_people == number_of_reacted_people:  break
            # 停滞がある程度続いてたら終了
            if stagnation_count > 60:
                print(f'        停滞してるので終了します。')
                break
            '''
            # low_limit <= dy <= up_limit の範囲で、残りの読み込めてない要素数に応じて、下にスクロール
            low_limit, up_limit = 5, 50
            # 今回新しくスクロールする分
            dy_of_scroll_this_time = low_limit + (up_limit - low_limit) * ((number_of_reacted_people - cur_count_reacted_people) / number_of_reacted_people)
            sum_dy_of_scroll += dy_of_scroll_this_time
            print(f'dy_of_scroll_down_this_time = {dy_of_scroll_this_time}   sum_dy_of_scroll = {sum_dy_of_scroll}')
            try:
                ActionChains(self.driver).drag_and_drop_by_offset(var_elem, 0, sum_dy_of_scroll).perform()
                print(f'var elem . x = {var_elem.location["y"]}')
            except:
                print('error in ActionChains.drag_and_drop_by_offset')
            sleep(0.35)
            '''

    def __get_urls_of_reacted_people_from_button_elem(
            self,
            display_button,  # クリックするとリアクションした人の一覧が表示されるボタン要素
    ) -> [str]:
        '''
        引数でもらった一覧を表示するボタンを押して、表示された人たちの URL をリストで返す関数
        '''
        urls = []
        # 今見てるボタン要素の部分のソースから、この投稿にリアクションした人の人数を取得
        number_of_reacted_people = self.__get_number_of_reacted_people_from_button_elem(display_button)
        # ボタンをクリックして一覧を表示
        self.driver.execute_script("arguments[0].click();", display_button)

        sleep(1)
        # すべての人がちゃんと読み込めるまで、スクロールとかをする
        self.__load_page_display_reacted_people_until_get_urls(number_of_reacted_people)
        urls = self.__get_top_page_urls_of_reacted_people_on_displayed_page()

        # 人たちのリンクのグループを一つにしておくために（開きっぱだと残ってしまう）今回のをちゃんと閉じとく
        close_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.CLOSE_BUTTON_ON_DISPLAYED_PAGE.replace(' ', '.'))
        self.driver.execute_script("arguments[0].click();", close_button)
        # 読み込んだ段階で、一覧で表示されてる人たちの URL を取得し返す
        return urls

    def __set_post_and_button_elems(
            self,
            target_top_page_url: str,       # 対象とする人の投稿の載ってるトップページ
            number_of_target_posts: int,    # 対象とする投稿の数
    ) -> None:
        '''
        調査対象の投稿を読み込んでいき、投稿の要素とボタンの要素と各ボタンのインデックス（リアクションした人たちのリンクが載ってるグループが今を確認するために）をセットする
        '''
        # セットするための各要素
        self.post_elems   = []
        self.button_elems = []
        self.post_index2button_index = {}
        # まず投稿の要素を取得
        self.post_elems = self.__get_post_elems_by_url(target_top_page_url, number_of_target_posts)
        # ボタン要素と、何番目の投稿が何番目のボタンに対応してるかの辞書を取得
        for i, post_elem in enumerate(self.post_elems):
            if self.__does_post_have_button_display_reacted_people(post_elem):
                # インデックスの変換を記録
                self.post_index2button_index[i] = len(self.button_elems)
                # ボタン要素を保存
                self.button_elems.append(post_elem.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.BUTTON_DISPLAY_REACTED_PEOPLE.replace(' ', '.')))

    def siori_test(self):
        self.__set_post_and_button_elems('https://www.facebook.com/minatoyasouken', 10)
        for i, button in enumerate(self.button_elems):
            print(f'{i} button')
            self.driver.execute_script("arguments[0].click();", button)
            link_list = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.GROUP_OF_DISPLAY_LIST.replace(' ', '.'))

            print('        ', link_list.text.replace('\n', ' '))

            r = 'oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn s45kfl79 emlxlaya bkmhp75w spb7xbtv rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv j83agx80 taijpn5t jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso l9j0dhe7 tv7at329 thwo4zme tdjehn4e'
            close_button = self.driver.find_element(by=By.CSS_SELECTOR, value='.'+r.replace(' ', '.'))
            self.driver.execute_script("arguments[0].click();", close_button)
            print('    close button pushed')


    def __get_post_elems_by_url(
            self, 
            target_top_page_url: str,       # 対象とする人の投稿の載ってるトップページ
            number_of_target_posts: int,    # 対象とする投稿の数
    ) -> []:
        '''
        調査対象の投稿を読み込んでいき、与えられた数だけ投稿要素を返す関数
        '''
        print('対象のページにアクセスしています ... ')
        self.driver.get(target_top_page_url)
        self.__print_done_message_with_sleep(2)

        print(f'投稿を読み込んでいます ... （取得する投稿の数 : {number_of_target_posts}）')
        post_elems = []  # 返り値
        # 欲しい投稿数分が取得されるまで、下にスクロールしてページを読み込む
        prv_posts_count, cur_posts_count, stagnation_count = -1, 0, 0
        page = self.driver.find_element(by=By.TAG_NAME, value='html')
        while stagnation_count < 60:
            # 今のすべての投稿の要素を取得
            post_elems = self.driver.find_elements(by=By.CSS_SELECTOR, value='.'+self.classnames.POSTS.replace(' ', '.'))
            cur_posts_count = len(post_elems)
            if cur_posts_count > prv_posts_count:
                print(f'    （読み込み中） 現在取得されている投稿数 : {cur_posts_count} / {number_of_target_posts}')
                prv_posts_count = cur_posts_count
                stagnation_count = 0
            else:
                stagnation_count += 1
            # 与えられた必要数を上回ってれば読み込み終了
            if cur_posts_count >= number_of_target_posts:  break

            # 下に読み込みを続けるだけだと、遅い時に余計遅い感じがするから、一旦上にも上げるようにしてる
            page.send_keys(Keys.PAGE_UP)
            sleep(0.4)
            for _ in range(20):  page.send_keys(Keys.PAGE_DOWN)
            sleep(max(1, min(2, number_of_target_posts - cur_posts_count)))  # 下限と上限を決めてその間でsleep
        self.__print_done_message_with_sleep(1)
        # 必要数ですりきって返す
        return post_elems[:number_of_target_posts]
        
    def login_to_facebook_top_page(self, my_email_or_number: str, my_password: str) -> None:
	# FACEBOOK のトップページにログインする
        print(f'FACEBOOK のトップページでログインしています ... ')
        self.driver.get(self.FACEBOOK_TOP_URL)
        # 入力欄の要素を取得
        email_or_number_elem = self.driver.find_element(by=By.NAME, value='email')
        password_elem        = self.driver.find_element(by=By.NAME, value='pass')
        # メアド・パスワードを入力
        email_or_number_elem.send_keys(my_email_or_number)
        password_elem.send_keys(my_password)
        # 入力した値でログイン
        password_elem.submit()
        sleep(2)
        if 'email' in self.driver.page_source and 'password' in self.driver.page_source:
            print('ログインに失敗しました。最初からやり直してください。プログラムを終了します。')
            exit(0)
        self.__print_done_message_with_sleep(2)
        
    def __get_driver(self, wait_time_until_find_elems: int=10) -> selenium.webdriver.chrome.webdriver.WebDriver:
        # 設定されたオプションと、もらった要素取得時の待機時間から、Chrome のドライバーを返す関数
        self.wait_time_until_find_elems = wait_time_until_find_elems
        print('Chrome を起動します ... ')
        driver = webdriver.Chrome(options=self.options)
        # これ以降のすべての要素取得動作に置いて、要素が見つかるまで、最大 wait_time 秒間待機する（実質読み込みを待つ動作）
        driver.implicitly_wait(wait_time_until_find_elems)
        self.__print_done_message_with_sleep(0.3)
        return driver

    def __get_options(self) -> selenium.webdriver.chrome.options.Options:
        # WebDriver のオプションを設定して返す関数
        options = webdriver.ChromeOptions()
        if self.is_mode_headless:  options.add_argument('--headless')        # 描画に関する設定
        options.add_argument("start-maximized")                              # 画面サイズを最大化
        prefs = {"profile.default_content_setting_values.notifications" : 2, # ポップアップ通知の無効化
                 "credentials_enable_service": False,                        # 下とともに、パスワードを保存するか確認するポップアップを非表示に
		 "profile.password_manager_enabled": False}
        options.add_experimental_option("prefs", prefs)
        return options


    # ここから下は、ヘルパー関数のような役割のもの

    def save_current_page_source(self, path_for_save: str):
	#  分析用に現時点でのソースを保存する
        with open(path_for_save, mode='w') as f:
            f.write(self.driver.page_source)
        print(f'ソースコードをセーブしました  保存場所 : {path_for_save}')

    def __get_number_of_reacted_people_from_button_elem(self, button_elem) -> int:
        """
        リアクションした人の一覧を表示するボタンの部分からその人数を取得する関数
        button_elem の中には人数をテキストに持つ要素が２つあるので、そのうち一つを指定して、そこから返す
        """
        elem_has_number = button_elem.find_element(by=By.CSS_SELECTOR, value='.'+self.classnames.HAS_NUMBER_IN_BUTTON_DISPLAY.replace(' ', '.'))
        try:
            # 対象の投稿数が 10 の時は.textからしても何もエラーが起きなかったが、 20 にした時にエラーが起きるようになった どちらもinnerHTMLからするとエラーは静まったのでとりあえず
            #ret = int(elem_has_number.text.replace(',', ''))
            ret = int(elem_has_number.get_attribute('innerHTML').replace(',', ''))
        except:
            print('ERROR  (in  __get_number_of_reacted_people_from_button_elem)')
            print(f'button_elem.innerHTML = {button_elem.get_attribute("innerHTML")}')
            print(f'elem_has_number.text = {elem_has_number.text}')
            print(f'elem_has_number.innerHTML = {elem_has_number.get_attribute("innerHTML")}')
        return ret

    @staticmethod
    def get_profile_page_url_from_top_page_url(top_page_url: str) -> str:
        '''
        その人のトップページのURLから基本データの載ってるページ（/about...）のURLを返す
        '''
        profile_page_url = top_page_url
        if r'profile.php?id=' in top_page_url:
            profile_page_url += '&sk=about'
        else:
            profile_page_url += '/about'
        return profile_page_url

    @staticmethod
    def __get_abs_top_page_url(top_page_url: str) -> str:
        '''
        必要ないクエリパラメータを消す その人のページにアクセスするために必要な文字列以外を切り捨てる感じ
        各種のURLを次の様に変換する

        >>> __get_abs_top_page_url('https://www.facebook.com/profile.php?id=id_of_target_person&.........')
        'https://www.facebook.com/profile.php?id=id_of_target_person'
        >>> __get_abs_top_page_url('https://www.facebook.com/lastname.middlename.firstname?.............')
        'https://www.facebook.com/lastname.middlename.firstname'
        '''
        FACEBOOK_TOP_URL = r'https://www.facebook.com/'
        MARK_OF_BY_ID = r'profile.php?id='
        # それぞれのパターン文字列を作成
        PATTERN_OF_BY_ID   = f'{FACEBOOK_TOP_URL}{MARK_OF_BY_ID}'
        PATTERN_OF_BY_NAME = f'{FACEBOOK_TOP_URL}'
        # ~php?id= までに含まれる文字列のうち正規表現で意味を持つもの（この場合.と?）をエスケープさせる
        # エスケープするために付け加えられる \ はそれ自身がエスケープ対象なので、一番最初にする
        for c in '\.?[]{}()^$|+*':
            PATTERN_OF_BY_ID   = PATTERN_OF_BY_ID.replace(c, f'\{c}')
            PATTERN_OF_BY_NAME = PATTERN_OF_BY_NAME.replace(c, f'\{c}')
        # 最後にどこまで取るかのための目印（& とか ?）と、その前に最小の長さで任意にヒットする（.*?）をくっつける
        PATTERN_OF_BY_ID   += '.*?\&'
        PATTERN_OF_BY_NAME += '.*?\?'
        # それぞれ検索 番兵としてそれぞれ停止文字を後ろに付けてる (不必要なクエリパラメータが全くついてない状態の時は、そのまま返したいから)
        searched_by_id   = re.search(PATTERN_OF_BY_ID, top_page_url+'&')
        searched_by_name = re.search(PATTERN_OF_BY_NAME, top_page_url+'?')
        abs_top_page_url = top_page_url
        if searched_by_id != None:
            # ID でページのURLが決まってるの
            # 'https://www.facebook.com/profile.php?id=.......&' までを取得し、最後の&を消す
            abs_top_page_url = searched_by_id.group()[:-1]
        elif searched_by_name != None:
            # USER NAME でページのURLが決まってるの
            # 'https://www.facebook.com/lastname.middlename.firstname?'までを取得し、最後の?を消す
            abs_top_page_url = searched_by_name.group()[:-1]
        else:
            # どちらにもマッチしなかった場合 エラー分だけ表示してそのまま返す
            print('error in get_abs_top_page_url. Neither pattern of by id and by name were matched! top_page_url = {top_page_url}')
        if abs_top_page_url[-1] == '/':  abs_top_page_url = abs_top_page_url[:-1]
        return abs_top_page_url    

    @staticmethod
    def __print_done_message_with_sleep(time_seconds=3):
        print('完了しました\n')
        sleep(time_seconds)


def sleep_with_print(t):
    print(f'start sleep {t}[sec] ... ', end='', flush=True)
    sleep(t)
    print('end')


def stop(mess: str = 'STOP  (press enter to resume)'):
    input(mess)



def main():
    if len(sys.argv) < 5:
        print('引数が足りません。以下の値を実行時に引数として入力してください。')
        print('[1] : ログインに使うメールアドレスまたは電話番号')
        print('[2] : ログインに使うパスワード')
        print('[3] : 対象とする投稿の数')
        print('[4] : 対象とする FaceBook のページ')
        print('[5] : 結果を保存するファイルのパス')
        return
    email_or_number  = sys.argv[1]       # ログインに使うメールアドレスまたは電話番号
    password         = sys.argv[2]       # ログインに使うパスワード
    number_of_posts  = int(sys.argv[3])  # 対象とする投稿の数
    target_url       = sys.argv[4]       # 対象とする FaceBook のページ
    answer_file_path = sys.argv[5]       # 結果を保存するファイルのパス

    scraper = FacebookScraper(
        email_or_number,
        password,
        False,
    )

    urls = scraper.get_urls_of_reacted_people(target_url, number_of_posts - 1, True)
    for i, url in enumerate(urls):
        print(f'urls[{i}] = {url}')
    return
    

    test_send_message_by_messenger_to_reacted_people(target_url, number_of_posts, scraper)

    return

    # [{{}}] の形で帰る [{リアクションした人のURL : {情報の項目名(名前とか) : その人の情報}}] で各投稿ごとにリストで
    info_dicts_of_reacted_people_per_posts = scraper.get_info_dicts_of_reacted_people_per_posts(target_url, number_of_posts)

    
    with open(answer_file_path, 'w') as f:
        json.dump(info_dicts_of_reacted_people_per_posts, f, indent=4, ensure_ascii=False)
    return 

    
if __name__ == '__main__':
    #doctest.testmod()
    main()



def test_get_urls_of_reacted_people_per_posts(target_url, number_of_posts, scraper):
    # 各投稿にリアクションした人たちの URL を取得するテスト
    urls_per_posts = scraper.get_urls_of_reacted_people_per_posts(target_url, number_of_posts)
    for i, urls in enumerate(urls_per_posts, start=1):
        print(f'投稿 {i} について')
        for j, url in enumerate(urls, start=1):
            print(f'    name: {scraper.url2fullname[url]}   url: {url}')
        print()
    return

def test_get_info_dict_by_top_page_url(url, scraper):
    # 個人のページで get_info_dict_by_top_page_url(url) をテスト
    info_dict = scraper.get_info_dict_by_top_page_url(url)
    with open('data_of_the_person.json', 'w') as f:
        json.dump(info_dict, f, indent=4, ensure_ascii=False)

def test_get_info_dicts_of_reacted_people_per_posts(target_url, number_of_posts, scraper):
    # 各投稿にリアクションした人たちの 情報 を取得するテスト
    info_dicts_of_reacted_people_per_posts = scraper.get_info_dicts_of_reacted_people_per_posts(target_url, number_of_posts)
    with open('info_dicts_of_reacted_people_per_posts.json', 'w') as f:
        json.dump(info_dicts_of_reacted_people_per_posts, f, indent=4, ensure_ascii=False)
    return 

def test_send_message_by_messenger_to_reacted_people(target_url, number_of_posts, scraper):
    # 各投稿にリアクション下人たちに、メッセージを送るテスト

    # scraper.url2fullname を蓄積させるために呼び出す
    scraper.get_urls_of_reacted_people_per_posts(target_url, number_of_posts)
    names_of_reacted_people = list(scraper.url2fullname.values())
    for i, name in enumerate(names_of_reacted_people):
        print(f'    宛先 {i:3}  :  {name}')
    print('以上の人たちを宛先に送るメッセージ画面を開きいています ...')
    scraper.send_message_by_messenger_to(names_of_reacted_people)
    return

def write_info_dicts_on_xl(info_dicts_of_reacted_people_per_posts: {}, xl_file_path: str) -> None:
    # xl_file_path のエクセルファイルに、リアクションした人たちの情報を書き込む
    import openpyxl
    # ブック・シートを取得
    wb = openpyxl.load_workbook(xl_file_path)
    sheet = wb['Sheet1']
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
    # 今の書き込む行
    row4write = 1
    # 各投稿ごとに
    for info_dicts_of_reacted_people in info_dicts_of_reacted_people_per_posts:
        # 各人ごとに
        for url, info_dict in info_dicts_of_reacted_people.items():
            # 各情報の項目ごとに
            for key, value in info_dict.items():
                sheet.cell(row=row4write, column=keyname2column[key], value=value)
            row4write += 1
        row4write += 1

    wb.save(xl_file_path)
    print('エクセルファイルに結果を出力しました。')

