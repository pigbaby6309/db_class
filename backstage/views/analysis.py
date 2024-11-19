from flask import render_template, Blueprint
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import Analysis

analysis = Blueprint('analysis', __name__, template_folder='../templates')

@analysis.route('/dashboard')
@login_required
def dashboard():
    revenue = []
    dataa = []
    for i in range(1,13):
        row = Analysis.month_price(i)

        if not row:
            revenue.append(0)
        else:
            for j in row:
                revenue.append(j[1])
        
        row = Analysis.month_count(i)
        
        if not row:
            dataa.append(0)
        else:
            for k in row:
                dataa.append(k[1])
    #---------------------------------------    
    #row = Analysis.category_sale()
    row = Analysis.author_sale()
    datab = []
    for i in row:
        temp = {
            'value': i[0],
            'name': i[1]
        }
        datab.append(temp)
    #-------------------------------
    row = Analysis.author_sale_count()
    datad = []
    for i in row:
        temp = {
            'value': i[1],
            'name': i[0]
        }
        datad.append(temp)
    #-------------------------------    
    row = Analysis.member_sale()
    datac = []
    nameList = []
    countList = []
    counter = 0
    
    for i in row:
        counter = counter + 1
        datac.append(i[0])
        nameList.append(i[1])
        countList.append(i[3])

    counter = counter - 1
    
    #row = Analysis.member_sale_count()
    
    #for i in row:
        #countList.append(i[0])
        
    return render_template('dashboard.html', counter = counter, revenue = revenue, dataa = dataa, \
                           datab = datab, datac = datac, datad = datad, nameList = nameList, countList = countList)