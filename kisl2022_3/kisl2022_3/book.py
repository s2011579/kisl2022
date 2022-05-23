"""
予約一覧・検索・予約を行う
"""

from datetime import datetime
from distutils.command.build import build
from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, session
)
from pyparsing import matchPreviousLiteral
from werkzeug.exceptions import abort
from kisl2022_3.auth import login_required
from kisl2022_3.db import get_db
import re

bp = Blueprint('book', __name__, url_prefix='/book')

@bp.route('/')
@login_required
def index_book():
    """予約の一覧を取得する"""

    # DBと接続
    db = get_db()

    # 予約データを取得
    user_id = session.get('user_id')

    if user_id ==1:
        all_books = db.execute(
            '''SELECT id, strftime('%Y/%m/%d',book_date) AS book_date,substr('日月火水木金土', strftime('%w',book_date)+1, 1) AS weekday,lecture,class_room,book_group,book_matter FROM book,lecture_division
            WHERE book.book_lecture = lecture_division.lecture_id ORDER BY book.book_date ASC, book.book_lecture ASC'''
        ).fetchall()

        return render_template('book/index_book.html',
                           books=all_books,
                           title='予約一覧',
                           year=datetime.now().year)


    books = db.execute(
        '''SELECT id, strftime('%Y/%m/%d',book_date) AS book_date,substr('日月火水木金土', strftime('%w',book_date)+1, 1) AS weekday,lecture,class_room,book_group,book_matter FROM book,lecture_division
         WHERE user_id = ? AND book.book_lecture = lecture_division.lecture_id ORDER BY book.book_date ASC, book.book_lecture ASC''', (user_id,)
    ).fetchall()

    # 予約一覧画面へ遷移
    return render_template('book/index_book.html',
                           books=books,
                           title='予約一覧',
                           year=datetime.now().year)

@bp.route('/searchcr')
@login_required
def searchcr():
    # flash('予約が追加されました', category='alert alert-info')
    return render_template('book/create_book.html',
                            title='教室検索',
                            year=datetime.now().year)


@bp.route('/cr', methods=["GET"])
@login_required
def create_book():
    # 検索フォームから送られてきた値を取得
    building = request.args.get('building')
    support_room = request.args.get('support_room')
    capacity = request.args.get('capacity')
    VTR = request.args.get('VTR')
    DVD = request.args.get('DVD')
    projector = request.args.get('Projector')
    OHP = request.args.get('OHP')
    screen = request.args.get('Screen')
    blackout_curtain = request.args.get('BlackoutCurtain')
    document_camera = request.args.get('DocumentCamera')
    automatic_recording = request.args.get('AutomaticRecording')
    remote_lecture = request.args.get('RemoteLecture')
    fixed_desk = request.args.get('FixedDesk')

    # DBと接続
    db = get_db()

    # エラーチェック
    error_message = None
    # if not title:
    #     error_message = '入力は必須です'
    if error_message is not None:
        # エラーがあれば、それを画面に表示させる
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('book.create_book'))

    # エラーがなければテーブルを検索する

    sql_cr = 'SELECT * FROM all_cr WHERE 1=1'
    sql_que = []
    if building != 'すべての教室棟':
        sql_cr += ' AND building = ?'
        sql_que.append(building)
    if support_room != 'すべてのエリア・支援室':
        sql_cr += ' AND support_room = ?'
        sql_que.append(support_room)
    if capacity != '':
        sql_cr += ' AND capacity >= ?'
        sql_que.append(capacity)
    if VTR == 'on':
        sql_cr += ' AND VTR = 1'
    if DVD == 'on':
        sql_cr += ' AND DVD = 1'    
    if projector == 'on':
        sql_cr += ' AND projector = 1'    
    if OHP == 'on':
        sql_cr += ' AND OHP = 1'
    if screen == 'on':
        sql_cr += ' AND screen = 1'
    if blackout_curtain == 'on':
        sql_cr += ' AND blackout_curtain = 1'
    if document_camera == 'on':
        sql_cr += ' AND document_camera = 1'
    if automatic_recording == 'on':
        sql_cr += ' AND automatic_recording = 1'
    if remote_lecture == 'on':
        sql_cr += ' AND remote_lecture = 1'
    if fixed_desk == 'on':
        sql_cr += ' AND fixed_desk = 1'

    results = db.execute(
        sql_cr, sql_que
    ).fetchall()
    
    # 検索結果一覧画面へ遷移
    # flash('検索されました', category='alert alert-info')
    return render_template('book/result_book.html',
                            title='検索結果',
                            results=results,
                            year=datetime.now().year)



@bp.route('/<class_room>')
@login_required
def check_book(class_room):
    # DBと接続
    db = get_db()
    # エラーチェック
    error_message = None
    error_check=[cr[0] for  cr in db.execute("SELECT class_room FROM all_cr").fetchall()]
    if class_room not in error_check:
        error_message = '入力した教室は存在しません'

    if error_message is not None:
        # エラーがあれば、それを画面に表示させる
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('book.searchcr'))

    check_results = db.execute(
        '''WITH RECURSIVE
        cnt(x) AS (VALUES(julianday('now','localtime')) UNION ALL SELECT x+1 FROM cnt WHERE x < julianday('now','localtime', '+35 days'))
        SELECT fweeks.datek,fweeks.date, fweeks.weekday, fweeks.lecture, crr.book_group, crr.book_matter, lecture_division.lecture AS lecture_div
        FROM (SELECT datek, date,weekday,column1 as lecture FROM (SELECT strftime('%Y-%m-%d',x) AS datek,strftime('%Y/%m/%d',x) AS date, substr('日月火水木金土', strftime('%w',x)+1, 1) AS weekday FROM cnt)
        CROSS JOIN (VALUES(1),(2),(3),(4),(5),(6),(7),(8),(9))) fweeks
        LEFT JOIN (SELECT strftime('%Y/%m/%d',book_date) AS book_datew,book_lecture,book_group,book_matter FROM book WHERE class_room = ? ) crr
        ON fweeks.date = crr.book_datew AND fweeks.lecture = crr.book_lecture, lecture_division WHERE fweeks.lecture = lecture_division.lecture_id''',
        (class_room,)
    ).fetchall()

    return render_template('book/check_book.html',
                            title= class_room+' 予約状況',
                            class_room=class_room,
                            check_results=check_results,
                            year=datetime.now().year)


@bp.route('/<book_classroom>/<book_date>/<book_lecture>', methods=('GET', 'POST'))
@login_required
def reserve_book(book_classroom, book_date, book_lecture):
    """
    GET ：書籍更新画面に遷移
    POST：書籍更新処理を実施
    """

    # 書籍データの取得と存在チェック
    # book = get_book_and_check(book_id)
    if request.method == 'GET':
        # DBと接続
        db = get_db()
        # エラーチェック
        error_message = None
        error_check=[cr[0] for  cr in db.execute("SELECT class_room FROM all_cr").fetchall()]
        if book_classroom not in error_check:
            error_message = '入力した教室は存在しません'

        if error_message is not None:
            # エラーがあれば、それを画面に表示させる
            flash(error_message, category='alert alert-danger')
            return redirect(url_for('book.searchcr'))
            
        reserve_date = datetime.strptime(book_date, '%Y-%m-%d').strftime('%Y/%m/%d')
        w_list = ['月', '火', '水', '木', '金', '土', '日']
        reserve_wday = w_list[datetime.weekday(datetime.strptime(book_date, '%Y-%m-%d'))]

        reserve_lecture=db.execute("SELECT lecture FROM lecture_division WHERE lecture_id = ?",(book_lecture)).fetchone()
        
        # 書籍更新画面に遷移
        return render_template('book/reserve_book.html',
                               book_classroom=book_classroom,
                               book_date=reserve_date,
                               book_wday=reserve_wday,
                               book_lecture=reserve_lecture,
                               title='予約申請',
                               year=datetime.now().year)
    # 書籍編集処理
    user_id = session.get('user_id')
    # 登録フォームから送られてきた値を取得
    book_group = request.form['book_group']
    book_matter = request.form['book_matter']
    # DBと接続
    db = get_db()

    # エラーチェック
    error_message = None

    if not book_group or not book_matter:
        error_message = '予約名義と予約内容の入力は必須です'

    if error_message is not None:
        # エラーがあれば、それを画面に表示させる
        flash(error_message, category='alert alert-danger')
        return redirect(url_for('book.reserve_book', book_classroom=book_classroom, book_date=book_date, book_lecture=book_lecture))

    # エラーがなければテーブルに登録する
    db.execute(
        'INSERT INTO book(user_id, book_date, book_lecture, class_room, book_group, book_matter) VALUES (?,?,?,?,?,?)',
        (user_id, book_date, book_lecture, book_classroom, book_group, book_matter)
    )
    db.commit()

    # 書籍一覧画面へ遷移
    flash('予約が追加されました', category='alert alert-info')
    return redirect(url_for('book.index_book'))


@bp.route('/<int:book_id>/delete_book', methods=('GET', 'POST'))
@login_required
def delete_book(book_id):
    """
    GET ：予約削除確認画面に遷移
    POST：予約削除処理を実施
    """
    # 予約データの取得
    db = get_db()

    book = db.execute(
        '''SELECT strftime('%Y/%m/%d',book_date) AS book_date,substr('日月火水木金土', strftime('%w',book_date)+1, 1) AS weekday, lecture,class_room,book_group,book_matter
        FROM book,lecture_division 
        WHERE id = ? AND book.book_lecture = lecture_division.lecture_id''', (book_id,)
    ).fetchone()

    if book is None:
        abort(404, 'There is no such book!!')

    if request.method == 'GET':
        # 予約削除確認画面に遷移
        return render_template('book/delete_book.html',
                               book=book,
                               title='予約の削除',
                               year=datetime.now().year)

    # 予約の削除処理
    db.execute('DELETE FROM book WHERE id = ?', (book_id,))
    db.commit()

    # 予約一覧画面へ遷移
    flash('書籍が削除されました', category='alert alert-info')
    return redirect(url_for('book.index_book'))


