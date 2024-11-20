from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
from datetime import datetime
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/product'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager = Blueprint('manager', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager.productManager'))

@manager.route('/productManager', methods=['GET', 'POST'])
@login_required
def productManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        pid = request.values.get('delete')
        data = Record.delete_check(pid)
        
        if(data != None):
            flash('failed')
        else:
            data = Product.get_product(pid)
            Product.delete_product(pid)
    
    elif 'edit' in request.values:
        pid = request.values.get('edit')
        return redirect(url_for('manager.edit', pid=pid))
    #---------------------------------------------------    241028
    elif 'po_edit' in request.values:
        pid = request.values.get('po_edit')
        return redirect(url_for('manager.cart', pid=pid))
    #---------------------------------------------------  241028


    book_data = book()
    return render_template('productManager.html', book_data = book_data, user=current_user.name)

def book():
    book_row = Product.get_all_product_2()
    book_data = []
    for i in book_row:
        book = {
            '商品編號': i[0],
            '商品名稱': i[1],
            '商品售價': i[5],
            '作者': i[3],
            '庫存': i[4],
            '供應商': i[6],
            '圖片網址': i[8]
        }
        book_data.append(book)
    return book_data

@manager.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            prd_no = en + number
            data = Product.get_product(prd_no)

        prd_name = request.values.get('prd_name')
        prd_price = request.values.get('prd_price')
        prd_author = request.values.get('prd_author')
        prd_stock = request.values.get('prd_stock')
        prd_publisher= request.values.get('prd_publisher')
        prd_desc = request.values.get('description')
        prd_img = request.values.get('prd_img')
        
        # 檢查是否正確獲取到所有欄位的數據
        #if prd_name is None or prd_price is None or prd_author is None or prd_stock is None or prd_publisher is None or prd_desc is None:
            #flash('所有欄位都是必填的，請確認輸入內容。')
            #return redirect(url_for('manager.productManager'))

        # 檢查欄位的長度
        #if len(prd_name) < 1 or len( prd_price) < 1:
            #flash('商品名稱或價格不可為空。')
            #return redirect(url_for('manager.productManager'))

        Product.add_product(
            {'prd_no' : prd_no,
             'prd_name' : prd_name,
             'prd_price' : prd_price,
             'prd_author' : prd_author,             
             'prd_stock' : prd_stock,
             'prd_publisher' : prd_publisher,
             'prd_desc':prd_desc,
             'prd_img':prd_img

            }
        )
        flash('You were successfully logged in')

        return redirect(url_for('manager.productManager'))

    return render_template('productManager.html')

@manager.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('bookstore'))

    if request.method == 'POST':
        Product.update_product(
            {
            'pname' : request.values.get('pname'),
            'price' : request.values.get('price'),
            'author' : request.values.get('author'), 
            'stock' : request.values.get('stock'), 
            'pdesc' : request.values.get('description'),
            'publisher' : request.values.get('publisher'),
            'pid' : request.values.get('pid'),
            'img' : request.values.get('prd_img')

            }
        )
        
        return redirect(url_for('manager.productManager'))

    else:
        product = show_info()
        return render_template('edit.html', data=product)


def show_info():
    pid = request.args['pid']
    data = Product.get_product(pid)
    pname = data[1]
    author = data[3]
    price = data[5]
    stock = data[4]
    publisher =data[6]
    description = data[2]
    image= data[8]

    product = {
        '商品編號': pid,
        '商品名稱': pname,
        '單價': price,
        '庫存': stock,
        '作者': author,
        '出版商': publisher,
        '商品敘述': description,
        '圖片網址': image
    }
    return product
#--------------------------------------------
@manager.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if request.method == 'GET':
        if (current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('manager.home'))
        if "pid" in request.args:
            data = Po_cart.get_po_cart(current_user.id)

            if data is None:  # 假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Po_cart.add_po_cart(current_user.id, time)  # 幫他加一台購物車
                data = Po_cart.get_po_cart(current_user.id)

            po_num = data[2]  # 取得交易編號
            #pid = request.form.get('pid')  # 使用者想要購買的東西，使用 `request.form.get()` 來避免 KeyError
            pid = request.args.get('pid')  # 使用者想要購買的東西，使用 `request.form.get()` 來避免 KeyError
            
            
            if not pid:
                flash('Product ID is missing.')
                return redirect(url_for('backstage.cart'))  # 返回購物車頁面並顯示錯誤信息

            # 檢查購物車裡面有沒有商品
            product = Record.check_po_product(pid, po_num)
            

            # 如果購物車裡面沒有的話，把它加一個進去
            if product is None:
                # 取得商品價錢
                price = Product.get_product(pid)[5]
                Record.add_po_product({'pid': pid, 'po_num': po_num, 'price': price, 'total': price})

            else:
                # 如果購物車裡面有的話，就多加一個進去
                price=product[3] #價格
                qty = Record.get_po_qty( po_num, pid)
                qty = qty+1
                total = (qty) * int(price)
                Record.update_po_product({'price': price ,'qty': qty , 'po_num':  po_num, 'pid': pid, 'total': total})

    # 回傳有 pid 代表要 加商品
    if request.method == 'POST':
    #if request.method == 'GET':
        if "pid" in request.form:
        #if "pid" in request.args:
            data = Po_cart.get_po_cart(current_user.id)

            if data is None:  # 假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Po_cart.add_po_cart(current_user.id, time)  # 幫他加一台購物車
                data = Po_cart.get_po_cart(current_user.id)

            po_num = data[2]  # 取得交易編號
            #pid = request.form.get('pid')  # 使用者想要購買的東西，使用 `request.form.get()` 來避免 KeyError
            pid = request.args.get('pid')  # 使用者想要購買的東西，使用 `request.form.get()` 來避免 KeyError
            
            if not pid:
                flash('Product ID is missing.')
                return redirect(url_for('backstage.cart'))  # 返回購物車頁面並顯示錯誤信息

            # 檢查購物車裡面有沒有商品
            product = Record.check_po_product(pid, po_num)
            # 取得商品價錢
            price = Product.get_product(pid)[5]

            # 如果購物車裡面沒有的話，把它加一個進去
            if product is None:
                Record.add_po_product({'pid': pid, 'po_num': po_num, 'price': price, 'total': price})
            else:
                # 如果購物車裡面有的話，就多加一個進去
                qty = Record.get_po_qty( po_num, pid)
                qty = qty+1
                total = (qty) * int(price)
                Record.update_po_product({'qty': qty , 'po_num':  po_num, 'pid': pid, 'total': total})

        elif "delete" in request.form:
            pid = request.form.get('delete')
            po_num = Po_cart.get_po_cart(current_user.id)[2]

            Member.delete_po_product(po_num, pid)
            product_data = only_cart()

        elif "po_edit" in request.form:
            change_order()
            return redirect(url_for('manager.productManager'))

        elif "purchase" in request.form:
            change_order()
            return redirect(url_for('manager.purchase'))

        elif "po_order" in request.form:
            po_num = Po_cart.get_po_cart(current_user.id)[2]

            #po_mun = Po_cart.get_po_cart(current_user.id)["po_num"]
            total = Record.get_po_total_money(po_num)
            prd_data=Record.get_po_pid(po_num)
            #publish = Product.get_product(prd_data)[3]
            #publish=prd_data[2]

            Po_cart.clear_po_cart(current_user.id)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_po_order({'mid': current_user.id,\
                                     'po_date': time, \
                                     'format': format,\
                                     'total': total,  \
                                     'po_num': po_num})
        
            return render_template('po_complete.html', user=current_user.name)

    product_data = only_cart()

    if product_data == 0:
        return render_template('po_empty.html', user=current_user.name)
    else:
        return render_template('po_cart.html', data=product_data, user=current_user.name)


#-----------------------------------------------------------

@manager.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)

@manager.route('/poManager', methods=['GET', 'POST'])
@login_required
def poManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_po_order()
        order_data = []
        for i in order_row:
            order = {
                '採購單編號': i[0],
                '採購人': i[1],
                '採購單總價': i[2],
                '採購時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_podetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '採購單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '採購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('poManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)

def only_cart():
    count = Po_cart.check(current_user.id)

    if count is None:
        return 0

    data = Po_cart.get_po_cart(current_user.id)
    po_num = data[2]
    product_row = Record.get_po_record(po_num)
    product_data = []

    for i in product_row:
        pid = i[1]
        pname = Product.get_name(i[1])
        price = i[3]
        qty = i[2]

        product = {
            '商品編號': pid,
            '商品名稱': pname,
            '商品價格': price,
            '數量': qty
        }
        product_data.append(product)

    return product_data

def change_order():
    data = Po_cart.get_po_cart(current_user.id)
    po_num = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    product_row = Record.get_po_record(data[2])

    for i in product_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格

        #if int(request.form[i[2]]) != i[3]:
            Record.update_po_product({
                'qty':request.form[i[1]],
                'pid':i[1],
                'price':request.form[i[1]+'_PRICE'], #修改後的價格
                'po_num':po_num,
                'total':int(request.form[i[1]])*int(request.form[i[1]+'_PRICE'])
            })
            print('change')

    return 0

@manager.route('/purchase')
def purchase():
    data = Po_cart.get_po_cart(current_user.id)
    po_num = data[2]

    product_row = Record.get_po_record(po_num)
    product_data = []

    for i in product_row:
        pname = Product.get_name(i[1])
        product = {
            '商品編號': i[1],
            '商品名稱': pname,
            '商品價格': i[3],
            '數量': i[2]
        }
        product_data.append(product)
    
    total = float(Record.get_po_total(po_num))  # 將 Decimal 轉換為 float


    return render_template('po_order.html', data=product_data, total=total, user=current_user.name)
