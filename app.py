from flask import Flask, render_template, jsonify
import feedparser
from datetime import datetime, timedelta
import requests as req
from xml.etree.ElementTree import *
import json
from googletrans import Translator
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
from datetime import datetime, timedelta
import re

app = Flask(__name__)


def filter_entries_within_five_days(entries):
    """日付が5日以内のエントリのみをフィルタリングする"""
    five_days_ago = datetime.now() - timedelta(days=5)
    filtered_entries = []

    for entry in entries:
        # エントリの公開日を解析
        if 'published_parsed' in entry:
            entry_date = datetime(*entry.published_parsed[:6])
            if entry_date > five_days_ago:
                filtered_entries.append(entry)

    return filtered_entries

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/rss/<path:url>')
def get_rss_feed(url):
    feed = feedparser.parse(url)
    filtered_entries = filter_entries_within_five_days(feed.entries)
    for entry in filtered_entries:
        entry['title'] = entry['title'].split(' - ')[0]
    # 重複のない辞書のリストを作る
    seen_titles = set()
    new_dict_list = []
    for d in filtered_entries:
        if d['title'][:7] not in seen_titles:
            new_dict_list.append(d)
            seen_titles.add(d['title'][:7])
    filtered_entries = new_dict_list
    
    # 'techrights' の URLで、タイトルに 'EPO' が含まれないエントリを削除
    if 'techrights' in url:
        filtered_entries = [entry for entry in filtered_entries if 'EPO' in entry['title']]

    # 英語の翻訳
    if 'ceid=US:en' in url or 'epo' in url or 'iam-media' in url or 'patentlyo' in url or 'techrights' in url or 'googlescholar' in url:
        translator = Translator()
        for entry in filtered_entries:
            entry['title'] = translator.translate(entry['title'], src='en', dest='ja').text
    # 中国語の翻訳
    if 'ceid=CN:zh-Hans' in url:
        translator = Translator()
        for entry in filtered_entries:
            entry['title'] = translator.translate(entry['title'], src='zh-cn', dest='ja').text
    # 韓国語の翻訳
    if 'ceid=KR%3Ako' in url:
        translator = Translator()
        for entry in filtered_entries:
            entry['title'] = translator.translate(entry['title'], src='ko', dest='ja').text
    return jsonify(filtered_entries)

@app.route('/api/rss/googlescholar')
def create_rss_feed_googlecholar():
    # Google Scholarの検索URL
    search_url = "https://scholar.google.com/scholar?hl=ja&scisbd=1&as_sdt=0%2C5&as_vis=1&q=allintitle%3A+patent+-%22Patent+Ductus%22+-%22Patent+Foramen%22+-%22patent+transjugular%22+-%22Patent+Blue+V%22&btnG="

    # ユーザーエージェントを設定してリクエスト送信
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    response = req.get(search_url, headers=headers)

    # レスポンスの内容をパース
    soup = BeautifulSoup(response.text, 'html.parser')

    # 結果を抽出
    results = soup.find_all('div', class_='gs_r gs_or gs_scl')

    # RSSフィードを作成
    fg = FeedGenerator()
    fg.title("Google Scholar Search Results")
    fg.link(href=search_url)
    fg.description("Google Scholar results for the query 'patent'.")

    # 日付計算用関数
    def parse_relative_date(relative_date_str):
        """Convert relative date (e.g., '1 日前') to absolute datetime."""
        match = re.match(r"(\d+)\s*日前", relative_date_str)
        if match:
            days_ago = int(match.group(1))
            return datetime.now() - timedelta(days=days_ago)
        return datetime.now()  # Default to current date if no match

    for result in results:
        title_tag = result.find('h3', class_='gs_rt')
        if title_tag and title_tag.a:
            title = title_tag.a.text
            link = title_tag.a['href']
            summary = result.find('div', class_='gs_rs').text if result.find('div', class_='gs_rs') else "No description available"
            pub_info = result.find('div', class_='gs_a').text if result.find('div', class_='gs_a') else "No publication info"
            
            # 日付の処理
            age_tag = result.find('span', class_='gs_age')
            if age_tag:
                pub_date = parse_relative_date(age_tag.text.strip())
            else:
                pub_date = datetime.now()

            # RSSアイテムを追加
            entry = fg.add_entry()
            entry.title(title)
            entry.link(href=link)
            entry.description(f"{summary} ({pub_info})")
            entry.pubDate(pub_date.strftime("%a, %d %b %Y %H:%M:%S +0000"))  # RSSフォーマットに変換

    rss_feed = fg.rss_str(pretty=True)
    return rss_feed

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8889)
