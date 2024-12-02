# RSS Reader
本プロジェクトは、複数のRSSフィードを効率的に収集・整理する<ins>一覧性のいい</ins>RSSリーダーアプリケーションです。さまざまなテーマの最新ニュースを簡単に取得し、日々の情報収集をより便利にします。
直感的なUIと軽量な設計で快適なユーザー体験を提供します。

## 特徴
- マルチRSSサポート: 複数のRSSフィードを統合的に管理。複数のRSSフィードをまとめて一つのRSSフィードとして扱うことも可能。
- 多言語翻訳: 記事タイトルを自動翻訳。
- レスポンシブデザイン: PCからスマートフォンまで最適化されたUI。

## セットアップ
1. 必要な依存ライブラリをインストールしてください / Please install the required dependency libraries.
   ```bash
   pip install flask feedparser googletrans
   ```

2. index.html内でRSSのURLを指定（Googleニュースがおすすめ）
```
// 複数のRSSフィードをロード（複数のRSSフィードをまとめて一つのRSSフィードとして扱うことも可能。）
loadRSS('feed1', ['URL1', 'URL', 'URL3']);
loadRSS('feed2', ["URL4"]);
loadRSS('feed3', ["URL5"]);
// 必要に応じてさらにフィードを追加
```

3. 必要に応じてapp.py内で翻訳するURLを指定

   以下はGoogleニュースのRSSフィードの例
```
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
```

4. Flaskサーバーを起動 / Start the Flask server.
   ```bash
   python app.py
   ```

## 免責事項 / Disclaimer
本プログラム（以下「本ソフトウェア」）は、現状有姿（"AS IS"）で提供されます。本ソフトウェアの使用に関する以下の事項をご了承ください。<br>
The program (hereinafter referred to as "the Software") is provided "AS IS". Please note the following terms regarding the use of the Software:
- 保証の否認: 本ソフトウェアは、明示的または黙示的を問わず、いかなる保証もなく提供されます。特定の目的への適合性、商品性、非侵害性に関する保証を含みますが、それに限定されません。
- 責任の制限: 本ソフトウェアの使用、または使用不能に起因する、いかなる損害（直接的、間接的、偶発的、特殊的、結果的損害を含むがこれに限らない）についても、著作者または権利保有者は一切の責任を負いません。
- 自己責任の原則: 本ソフトウェアの使用は、すべてユーザー自身の責任において行われるものとします。本ソフトウェアの使用によって生じた問題について、著作者または権利保有者は一切の責任を負いません。
