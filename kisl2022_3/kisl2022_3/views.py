"""
FlaskアプリケーションのRouteとView
"""

from datetime import datetime
from flask import render_template
from kisl2022_3 import app

@app.route('/')
@app.route('/home')
def home():
    """インデックスページの表示"""
    return render_template(
        'index.html',
        title='トップページ',
        year=datetime.now().year,
    )