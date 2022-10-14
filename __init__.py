from flask import Flask
app = Flask(__name__)
# 同じディレクトリ内のモジュールのimportはパッケージ名から書いた方がいい。
# import (パッケージ名).(モジュール名)
import flaskr.main #main.pyを追加