# _*_ coding: utf-8 _*_
from models import User, Weibo, Comment
from routes.session import session
from utils import redirect, http_response, template, error, response_with_headers

__author__ = 'lv'
__date__ = '2017/12/11 14:54'


def current_user(request):
    session_id = request.cookies.get('user', '')
    user_id = session.get(session_id, -1)
    return user_id


def index(request):

    user_id = request.query.get('user_id',-1)
    user_id = int(user_id)
    user = User.find(user_id)
    print('user_id',user_id)
    if user is None:
        return redirect('/login')

    weibos = Weibo.find_all(user_id=user_id)
    body = template('weibo_index.html', weibos=weibos, user=user)
    return http_response(body)


def new(request):
    uid = current_user(request)
    user = User.find(uid)
    body = template('weibo_new.html')
    return http_response(body)


def add(request):
    uid = current_user(request)
    user = User.find(uid)

    form = request.form()
    w = Weibo(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def add(request):
    uid = current_user(request)
    user = User.find(uid)

    form = request.form()
    w = Weibo(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))


def login_required(route_function):
    def func(request):
        uid = current_user(request)
        if uid == -1:
            return redirect('/login')
        else:
            return route_function(request)
    return func


def delete(request):
    uid = current_user(request)
    user = User.find(uid)
    # 删除微博
    weibo_id = request.query.get('id', None)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    w.delete(weibo_id)
    return redirect('/weibo/index?user_id={}'.format(user.id))

def edit(request):
    weibo_id = request.query.get('id', -1)
    weibo_id = int(weibo_id)
    w = Weibo.find(weibo_id)
    if w is None:
        return error(request)
    # 生成一个 edit 页面
    body = template('weibo_edit.html',
                    weibo_id=w.id,
                    weibo_content=w.content)
    return http_response(body)


def update(request):
    uid = current_user(request)


    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    print('weibo_id_____________', weibo_id)
    w = Weibo.find(weibo_id)
    print('w.user_id_____________', w.user_id)
    if uid != w.user_id:
        return error(request)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo/index?user_id={}'.format(uid))


def comment_add(request):
    headers = {
        'Content-Type': 'text/html',
    }
    uid = current_user(request)
    header = response_with_headers(headers)
    user = User.find(uid)
    # 创建微博
    form = request.form()
    w = Comment(form)
    w.user_id = user.id
    w.save()
    return redirect('/weibo/index?user_id={}'.format(user.id))

route_dict = {
    '/weibo/index': index,
    '/weibo/new': login_required(new),
    '/weibo/edit': login_required(edit),
    '/weibo/add': login_required(add),
    '/weibo/update': login_required(update),
    '/weibo/delete': login_required(delete),
    # # 评论功能
    '/comment/add': login_required(comment_add),
}