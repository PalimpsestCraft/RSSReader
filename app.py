from flask import Flask, render_template, jsonify
import feedparser
from datetime import datetime, timedelta
from googletrans import Translator

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
    
    # 英語の翻訳
    if 'ceid=US:en' in url:
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

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=8888)
