import imp
import re
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

class User(UserMixin):
    pass

def is_valid_email(email):
    pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return True if pattern.match(email) else False

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    data = Member.get_role(userid)
    try:
        user.role = data[0]
        user.name = data[1]
    except:
        pass
    return user

@api.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':

        account = request.form['account']
        password = request.form['password']
        data = Member.get_member(account) 

        try:
            DB_password = data[0][1]
            user_id = data[0][2]
            identity = data[0][3]

        except:
            flash('*沒有此帳號')
            return redirect(url_for('api.login'))

        if(DB_password == password ):
            user = User()
            user.id = user_id
            login_user(user)

            if( identity == 'user'):
                return redirect(url_for('bookstore.bookstore'))
            else:
                return redirect(url_for('manager.productManager'))
        
        else:
            flash('*密碼錯誤，請再試一次')
            return redirect(url_for('api.login'))

    
    return render_template('login.html')

@api.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user_account = request.form['account']
        if not is_valid_email(user_account):
           flash('email 格式不正確') 
           return redirect(url_for('api.register'))
        
        user_name = request.form['username']
        #exist_account = Member.get_all_account()
        exist_account=Member.check_account_username(user_account,user_name)

        if (len(exist_account)!=0):
            account_list = []
            name_list = []
            s_str=""
            for i in exist_account:
                account_list.append(i[0])
                name_list.append(i[1])

            if (user_account in account_list):
                s_str=s_str+'email己存在!!'
            if (user_name in name_list):
                s_str=s_str+'暱稱己存在!!'
            flash(s_str)    
            return redirect(url_for('api.register'))
        else:
            input = { 
                'name': user_name, 
                'account':user_account, 
                'password':request.form['password'], 
                'identity':request.form['identity'],
                'birthday':request.form['birthday'],
                'tel':request.form['phone'],
                'addr':request.form['address']
            }
            Member.create_member(input)
            return redirect(url_for('api.login'))

    return render_template('register.html')

@api.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))