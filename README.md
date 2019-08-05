# Todoリスト

## 使用した技術要素
- Python 3.7.4
- Django 2.2.3
- sqlparse 0.3.0

## 開発環境のセットアップ
1. Windows Subsystem for Linuxのインストール
    - Microsoft StoreからUbuntuをインストールしてください
    - 参考: https://qiita.com/Aruneko/items/c79810b0b015bebf30bb
1. Python 3.7.4のインストール
    - 参考: https://www.python.jp/install/ubuntu/index.html
1. venvを用いた仮想環境の作成
    - 参考: https://qiita.com/fiftystorm36/items/b2fd47cf32c7694adc2e
1. Djangoのインストール
     - `pip install Django`を実行してインストール
     - 参考: https://docs.djangoproject.com/ja/2.2/intro/install/
1. その他必要なパッケージのインストール
    - `pip install sqlparse`
    - djangoでmigrateする際に必要になるパッケージ
    - 参考: https://qiita.com/SUKIYAPI/items/8c64425ecd74aff4e047


## 全体の設計・構成
| 機能 | 概要 |
----|---- 
| ToDoリスト作成 | タイトルを入力してToDoリストを作成 |
| ToDo作成 | タイトル，期限，メモ(任意)を入力してタスクを作成する |
| 検索 | ToDoリストとToDoのタイトルから検索ワードに合致する物を表示する |