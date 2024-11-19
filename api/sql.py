from typing import Optional
import psycopg2
from psycopg2 import pool


class DB:
    connection_pool = pool.SimpleConnectionPool(
        1, 100,  # 最小和最大連線數
       user='project_10',
       password='bmibxk',
       host='140.117.68.66',
       port='5432',
       dbname='project_10'
#      user='postgres',
#      password='postgres',
#      host='localhost',
#      port='5432',
#      dbname='project_10'
    )

    @staticmethod
    def connect():
        return DB.connection_pool.getconn()

    @staticmethod
    def release(connection):
        DB.connection_pool.putconn(connection)

    @staticmethod
    def execute_input(sql, input):
        if not isinstance(input, (tuple, list)):
            raise TypeError(f"Input should be a tuple or list, got: {type(input).__name__}")
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                connection.commit()
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def execute(sql):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
        except psycopg2.Error as e:
            print(f"Error executing SQL: {e}")
            connection.rollback()
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchall(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchall()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)

    @staticmethod
    def fetchone(sql, input=None):
        connection = DB.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, input)
                return cursor.fetchone()
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            raise e
        finally:
            DB.release(connection)


class Member:
    @staticmethod
    def get_member(account):
        sql = "SELECT account, password, mid, identity, name FROM member WHERE account = %s"
        return DB.fetchall(sql, (account,))

    @staticmethod
    def get_all_account():
        sql = "SELECT account FROM member"
        return DB.fetchall(sql)
    
    def check_account_username(account,username):
        sql = "SELECT account,name FROM member where account=%s or name=%s"
        return DB.fetchall(sql, (account,username,))

    @staticmethod
    def create_member(input_data):
        sql = 'INSERT INTO member (name, account, password, identity,tel,addr,birthday) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        DB.execute_input(sql, (input_data['name'], input_data['account'], input_data['password'], input_data['identity']\
                               ,input_data['tel'],input_data['addr'],input_data['birthday']))
        

    @staticmethod
    def delete_product(tno, pid):
        sql = 'DELETE FROM order_d WHERE trans_no = %s and prd_no = %s'
        DB.execute_input(sql, (tno, pid))

    def delete_po_product(po_num, pid):
        sql = 'DELETE FROM poitem_mst WHERE po_num = %s and prd_no = %s'
        DB.execute_input(sql, (po_num, pid))

    @staticmethod
    def get_order(userid):
        sql = 'SELECT * FROM order_m WHERE mid = %s ORDER BY order_date DESC'
        return DB.fetchall(sql, (userid,))

    def get_po(userid):
        #sql = 'SELECT * FROM po_mst WHERE mid = %s ORDER BY order_date DESC'
        sql = 'SELECT * FROM po_mst ORDER BY po_date DESC'
        #return DB.fetchall(sql, (userid,))
        return DB.fetchall(sql)
    
    @staticmethod
    def get_role(userid):
        sql = 'SELECT identity, name FROM member WHERE mid = %s'
        return DB.fetchone(sql, (userid,))


class Cart:
    @staticmethod
    def check(user_id):
        sql = '''SELECT * FROM cart, order_d 
                 WHERE cart.mid = %s::bigint 
                 AND cart.trans_no = order_d.trans_no::bigint'''
        return DB.fetchone(sql, (user_id,))

    @staticmethod
    def get_cart(user_id):
        sql = 'SELECT * FROM cart WHERE mid = %s'
        return DB.fetchone(sql, (user_id,))

    @staticmethod
    def add_cart(user_id, time):
        sql = 'INSERT INTO cart (mid, carttime, trans_no) VALUES (%s, %s, nextval(\'cart_tno_seq\'))'
        DB.execute_input(sql, (user_id, time))

    @staticmethod
    def clear_cart(user_id):
        sql = 'DELETE FROM cart WHERE mid = %s'
        DB.execute_input(sql, (user_id,))

    def clear_po_cart(user_id):
        sql = 'DELETE FROM po_cart WHERE mid = %s'
        DB.execute_input(sql, (user_id,))


class Po_cart:
    @staticmethod
    def check(user_id):
        sql = '''SELECT * FROM po_cart, poitem_mst 
                 WHERE po_cart.mid = %s::bigint 
                 AND po_cart.po_num = poitem_mst.po_num'''
        return DB.fetchone(sql, (user_id,))

    @staticmethod
    def get_po_cart(user_id):
        sql = 'SELECT * FROM po_cart WHERE mid = %s'
        return DB.fetchone(sql, (user_id,))

    @staticmethod
    def add_po_cart(user_id, time):
        sql = 'INSERT INTO po_cart (mid, carttime, po_num) VALUES (%s, %s, nextval(\'po_tno_seq\'))'
        DB.execute_input(sql, (user_id, time))

    @staticmethod
    def clear_po_cart(user_id):
        sql = 'DELETE FROM po_cart WHERE mid = %s'
        DB.execute_input(sql, (user_id,))

class Product:
    @staticmethod
    def count():
        sql = 'SELECT COUNT(*) FROM product'
        return DB.fetchone(sql)

    @staticmethod
    def get_product(prd_no):
        sql = 'SELECT * FROM product WHERE prd_no = %s'
        return DB.fetchone(sql, (prd_no,))

    @staticmethod
    def get_all_product():
        #只選擇有庫存的資料
        sql = 'SELECT * FROM product where prd_stock >0' 
        return DB.fetchall(sql)
    
    def get_all_product_2():
        #只選擇有庫存的資料
        sql = 'SELECT * FROM product' 
        return DB.fetchall(sql)

    @staticmethod
    def get_name(pid):
        sql = 'SELECT prd_name FROM product WHERE prd_no = %s'
        return DB.fetchone(sql, (pid,))[0]

    @staticmethod
    def add_product(input_data):
        #sql = 'INSERT INTO product (pid, pname, price, category, pdesc) VALUES (%s, %s, %s, %s, %s)'
        #DB.execute_input(sql, (input_data['pid'], input_data['pname'], input_data['price'], input_data['category'], input_data['pdesc']))        
        #sql = 'INSERT INTO product (prd_no, prd_name, prd_author,prd_price, prd_stock, prd_publisher,prd_desc) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        sql = 'INSERT INTO product (prd_no, prd_name,prd_author,prd_price, prd_stock, prd_publisher,prd_desc) VALUES (%s, %s, %s, %s, %s, %s, %s)'
        DB.execute_input(sql, (input_data['prd_no'],input_data['prd_name'],input_data['prd_author'],input_data['prd_price'],\
                               input_data['prd_stock'],input_data['prd_publisher'],input_data['prd_desc']))

    @staticmethod
    def delete_product(prd_no):
        sql = 'DELETE FROM product WHERE prd_no = %s'
        DB.execute_input(sql, (prd_no,))

    @staticmethod
    def update_product(input_data):
        #sql = 'UPDATE product SET pname = %s, price = %s, category = %s, pdesc = %s WHERE pid = %s'
        #DB.execute_input(sql, (input_data['pname'], input_data['price'], input_data['category'], input_data['pdesc'], input_data['prd_no']))
        sql='UPDATE product SET prd_name = %s,prd_author = %s,prd_price = %s,prd_stock = %s,prd_publisher = %s,prd_desc = %s WHERE prd_no = %s'
        DB.execute_input(sql, (input_data['pname'],input_data['author'],input_data['price'],input_data['stock'],\
                               input_data['publisher'],input_data['pdesc'],input_data['pid']))


class Record:
    @staticmethod
    def get_total_money(tno):
        sql = 'SELECT SUM(total) FROM order_d WHERE trans_no = %s'
        return DB.fetchone(sql, (tno,))[0]
    
    def get_po_total_money(po_num):
        sql = 'SELECT SUM(total) FROM poitem_mst WHERE po_num = %s'
        return DB.fetchone(sql, (po_num,))[0]
    
    def get_po_pid(po_num):
        sql = 'SELECT pm.po_num,pm.prd_no,pr.prd_publisher FROM poitem_mst pm \
               join product pr on pm.prd_no=pr.prd_no where pm.po_num=%s'
        return DB.fetchone(sql, (po_num,))

    @staticmethod
    def check_product(pid, tno):
        sql = 'SELECT * FROM order_d WHERE prd_no = %s and trans_no = %s'
        return DB.fetchone(sql, (pid, tno))

    def check_po_product(pid, po_num):
        sql = 'SELECT * FROM poitem_mst WHERE prd_no = %s and po_num = %s'
        return DB.fetchone(sql, (pid, po_num))

    @staticmethod
    def get_price(pid):
        sql = 'SELECT price FROM product WHERE pid = %s'
        return DB.fetchone(sql, (pid,))[0]

    @staticmethod
    def add_product(input_data):
        sql = 'INSERT INTO order_d (prd_no, trans_no, amount, saleprice, total) VALUES (%s, %s, 1, %s, %s)'
        DB.execute_input(sql, (input_data['pid'], input_data['tno'], input_data['saleprice'], input_data['total']))

    def add_po_product(input_data):
        sql = 'INSERT INTO poitem_mst (po_num,prd_no, qty, price, total) VALUES (%s, %s, 1, %s, %s)'
        DB.execute_input(sql, (input_data['po_num'],input_data['pid'], input_data['price'], input_data['total']))
        

    @staticmethod
    def get_record(tno):
        sql = 'SELECT * FROM order_d WHERE trans_no = %s'
        return DB.fetchall(sql, (tno,))

    @staticmethod
    def get_po_record(po_num):
        sql = 'SELECT * FROM poitem_mst WHERE po_num = %s'
        return DB.fetchall(sql, (po_num,))
    @staticmethod
    def get_amount(tno, pid):
        sql = 'SELECT amount FROM order_d WHERE trans_no = %s and prd_no = %s'
        return DB.fetchone(sql, (tno, pid))[0]
    
    def get_po_qty(po_num, pid):
        sql = 'SELECT qty FROM poitem_mst WHERE po_num = %s and prd_no = %s'
        return DB.fetchone(sql, (po_num, pid))[0]
    @staticmethod
    def update_product(input_data):
        sql = 'UPDATE order_d SET amount = %s, total = %s WHERE prd_no = %s and trans_no = %s'
        DB.execute_input(sql, (input_data['amount'], input_data['total'], input_data['pid'], input_data['tno']))

    def update_po_product(input_data):
        sql = 'UPDATE poitem_mst SET price=%s ,qty = %s, total = %s WHERE prd_no = %s and po_num = %s'
        DB.execute_input(sql, (input_data['price'],input_data['qty'], input_data['total'], input_data['pid'], input_data['po_num']))

    @staticmethod
    def delete_check(pid):
        sql = 'SELECT * FROM order_d WHERE prd_no = %s'
        return DB.fetchone(sql, (pid,))

    @staticmethod
    def get_total(tno):
        sql = 'SELECT SUM(total) FROM order_d WHERE trans_no = %s'
        return DB.fetchone(sql, (tno,))[0]
    
    def get_po_total(po_num):
        sql = 'SELECT SUM(total) FROM poitem_mst WHERE po_num = %s'
        return DB.fetchone(sql, (po_num,))[0]


class Order_List:
    @staticmethod
    def add_order(input_data):
        sql = 'INSERT INTO order_m (oid, mid, order_date, price, trans_no) VALUES (DEFAULT, %s, TO_TIMESTAMP(%s, %s), %s, %s)'
        DB.execute_input(sql, (input_data['mid'], input_data['order_date'], input_data['format'], input_data['total'], input_data['tno']))
        sql = 'update product as p set prd_stock =prd_stock-r.amount from order_d as r where r.prd_no=p.prd_no and r.trans_no= %s::bigint'
        DB.execute_input(sql, (input_data['tno'],))

    def add_po_order(input_data):
        #sql = 'INSERT INTO po_mst (po_num, po_date, publish) VALUES (DEFAULT, %s, TO_TIMESTAMP(%s, %s), %s, %s)'
        sql = 'INSERT INTO po_mst (po_num, po_date, totalprice, mid) VALUES(%s,TO_TIMESTAMP(%s, %s), %s, %s)'
        DB.execute_input(sql, (input_data['po_num'], input_data['po_date'], input_data['format'], \
                               input_data['total'], input_data['mid']))
            
        sql = 'update product as p set prd_stock =prd_stock+r.qty from poitem_mst as r where r.prd_no=p.prd_no and r.po_num= %s::bigint'
        DB.execute_input(sql, (input_data['po_num'],))

    @staticmethod
    def get_order():
        sql = '''
            SELECT o.oid, m.name, o.price, o.order_date
            FROM order_m o
            NATURAL JOIN member m
            ORDER BY o.order_date DESC
        '''
        return DB.fetchall(sql)
    def get_po_order():
        sql = '''
            select pm.po_num,m.name,pm.totalprice,pm.po_date from po_mst pm
            join "member" m on m.mid=pm.mid
            ORDER BY pm.po_date DESC,po_num desc
        '''
        return DB.fetchall(sql)

    @staticmethod
    def get_orderdetail():
        sql = '''
        SELECT o.oid, p.prd_name, r.saleprice, r.amount
        FROM order_m o
        JOIN order_d r ON o.trans_no = r.trans_no -- 確保兩者都是 bigint 類型
        JOIN product p ON r.prd_no = p.prd_no
        '''
        return DB.fetchall(sql)
    def get_podetail():
        sql = '''
        select pm.po_num,p.prd_name,pd.price,pd.qty from po_mst pm 
        join poitem_mst pd on pm.po_num=pd.po_num
        JOIN product p ON pd.prd_no = p.prd_no 

        '''
        return DB.fetchall(sql)


class Analysis:
    @staticmethod
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM order_date), SUM(price) FROM order_m WHERE EXTRACT(MONTH FROM order_date) = %s GROUP BY EXTRACT(MONTH FROM order_date)'
        return DB.fetchall(sql, (i,))

    @staticmethod
    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM order_date), COUNT(oid) FROM order_m WHERE EXTRACT(MONTH FROM order_date) = %s GROUP BY EXTRACT(MONTH FROM order_date)'
        return DB.fetchall(sql, (i,))

    @staticmethod
    def category_sale():
        sql = 'SELECT SUM(total), category FROM product, order_d WHERE product.prd_no = record.prd_no GROUP BY category'
        return DB.fetchall(sql)
    
    def author_sale():
        sql = 'SELECT SUM(total), prd_author FROM product, order_d WHERE product.prd_no = order_d.prd_no GROUP BY prd_author'
        return DB.fetchall(sql)

    @staticmethod
    def member_sale():
        #sql = 'SELECT SUM(price), member.mid, member.name FROM order_m, member WHERE order_m.mid = member.mid AND member.identity = %s GROUP BY member.mid, member.name ORDER BY SUM(price) DESC'
        sql = 'SELECT SUM(price), member.name, member.mid,count(*) FROM order_m, member WHERE order_m.mid = member.mid AND member.identity = %s GROUP BY member.mid, member.name '
        return DB.fetchall(sql, ('user',))

    @staticmethod
    def member_sale_count():
        sql = 'SELECT COUNT(*), member.mid, member.name FROM order_m, member WHERE order_m.mid = member.mid AND member.identity = %s GROUP BY member.mid, member.name ORDER BY COUNT(*) DESC'
        return DB.fetchall(sql, ('user',))
    
    @staticmethod
    def author_sale_count():
        sql='select p.prd_author,sum(d.amount) from order_d d join product p on p.prd_no =d.prd_no group by p.prd_author'
        return DB.fetchall(sql)

