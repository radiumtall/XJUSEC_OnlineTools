from  flask import render_template,Blueprint,redirect,url_for,flash,request,session
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required,current_user
from application.Form import Login_Form,Action_Arg,HttpMethod,NamePayload
from application.UserDb import Users
from application.XssDb import Xss,db
from application.config import *
from application.data import *
import os.path
import json
import datetime
from application.Safe import *
from application.BlogInDb import *
from application.BlogDb import Blog
import html

XJUSEC=Blueprint('my_web',__name__)

@XJUSEC.route('/welcome')
def index():
    # print(session)
    try:
        if  current_user.is_authenticated:
            return render_template('appliacation/index.html',name=session['name'])
        else:
            return redirect(url_for('my_web.login'))
            # return "login"
    except Exception as  e:
        # return redirect(url_for('my_web.login'))
        return e
@XJUSEC.route('/login')
def login():
    form = Login_Form()
    return render_template('appliacation/login.html', form=form)

@XJUSEC.route('/check_login',methods=['GET','POST'])
def check_login():
    if request.method == "POST":
        form = Login_Form()
        username = form.name.data
        passwd = form.pwd.data
        # print(username+passwd)
        if username!="" and passwd != "":
            user = Users.query.filter_by(username_xjusec=username).first()
            if user is not  None and user.passwd_xjusec==passwd:
                # flash('登录成功')
                login_user(user)
                session['name'] = username
                return redirect(url_for('my_web.index'))
            else:
                # flash('用户或密码错误')
                return redirect(url_for('my_web.login'))
        else:
            return  render_template('hack.html')

    else:
        return render_template('hack.html')

@XJUSEC.route('/logout')
@login_required
def logout():
    logout_user()
    flash('你已退出登录')
    return redirect(url_for('index'))

@XJUSEC.route('/webblog')
def web():
    if current_user.is_authenticated:
        action = request.args.get('type')
        if action == "reload":
            # get4hou()
            # getFreebuf()
            # getGlzjin()
            # getSeebug()
            # getYlg()
            try:
                getAllData()
                msg = '[xjusec]：{}'.format("All data update")
            except Exception as e:
                msg = '[xjusec]：{}'.format(e)
            show_4hou,show_Freebuf,show_Glzjin,show_Seebug,show_Ylg = show_data_limit(3)
            all_data ={}
            all_data['4hou'] = show_4hou
            all_data['Freebuf'] = show_Freebuf
            all_data['Glzjin'] = show_Glzjin
            all_data['Seebug'] = show_Seebug
            all_data['Ylg'] = show_Ylg
            return render_template('appliacation/web_blog.html',action="new",blogs = BLOGS,message=msg,alldata=all_data)
        if action == "new":
            msg = ""
            show_4hou, show_Freebuf, show_Glzjin, show_Seebug, show_Ylg = show_data_limit(3)
            all_data = {}
            all_data['4hou'] = show_4hou
            all_data['Freebuf'] = show_Freebuf
            all_data['Glzjin'] = show_Glzjin
            all_data['Seebug'] = show_Seebug
            all_data['Ylg'] = show_Ylg
            # print(all_data)
            return render_template('appliacation/web_blog.html',action=action,blogs = BLOGS,mssage=msg,alldata=all_data)
        if action == "all":
            msg = ""
            show_4hou, show_Freebuf, show_Glzjin, show_Seebug, show_Ylg = show_data_all()
            all_data = {}
            all_data['4hou'] = show_4hou
            all_data['Freebuf'] = show_Freebuf
            all_data['Glzjin'] = show_Glzjin
            all_data['Seebug'] = show_Seebug
            all_data['Ylg'] = show_Ylg
            # print(all_data)
            return render_template('appliacation/web_blog.html',action=action,blogs = BLOGS,mssage=msg,alldata=all_data)
    else:
        return redirect(url_for('my_web.login'))

# @XJUSEC.route('/xss')
# def xsser():
#     if current_user.is_authenticated:
#         load_data={}
#         with open(xss_data_path + '/' + xss_data_name.format(datetime.date.today().strftime('%y%m%d')), "r",
#                   encoding='utf-8') as file_r:
#             # load_data = json.load(open(xss_data_path+'/'+xss_data_name.format(datetime.date.today().strftime('%y%m%d'))))
#             #     print(type(file_r))
#             try:
#                 load_data = json.load(file_r)
#                 num = len(load_data)
#             except:
#                 num=0
#             id_list = []
#             for i in range(num):
#                 id_list.append(str(i+1))
#         return render_template('xss.html',id_list=id_list,load_data=load_data,action="xsser")
#     else:
#         return redirect(url_for('my_web.login'))
@XJUSEC.route('/xss',methods=['GET','POST'])
def xsser():
    if current_user.is_authenticated:
        action = "all"
        # time = str(datetime.date.today())
        num = 0
        id_list= []
        load_data={}
        form = Action_Arg()

        # if form.action.data and form.arg.data:
            # action = form.action.data
            # arg = form.arg.data
            # if action == "time":
            #     time = arg
            # print(action+arg)
        if action == "all":
            xss_data = Xss.query.all()
        if action == "time":
            xss_data = Xss.query.filter(Xss.time.like("%"+time+"%" if time is not None else "")).all()
        if action == "url":
            xss_data = Xss.query.filter(Xss.url.like("%"+arg+"%" if arg is not None else "")).all()
        if action == "ip":
            xss_data = Xss.query.filter(Xss.ip.like("%"+arg+"%" if arg is not None else "")).all()
        if action == "cookie":
            xss_data = Xss.query.filter(Xss.cookie.like("%"+arg+"%" if arg is not None else "")).all()
        for i in xss_data:
            num += 1
            data = {}
            data['url'] = i.url
            data['ip'] = i.ip
            data['time'] = i.time
            data['cookie'] = i.cookie
                # print(data)
            load_data[str(num)]=data
        # print(load_data)
        for j in range(num):
            id_list.append(str(j+1))
        return render_template('appliacation/xss.html',id_list=id_list,load_data=load_data,form=form)
    else:
        return redirect(url_for('my_web.login'))


@XJUSEC.route('/sqli')
def sqli():
    if current_user.is_authenticated:
        return render_template('appliacation/sqli.html')
    else:
        return redirect(url_for('my_web.login'))
@XJUSEC.route('/httpMethod',methods=['GET','POST'])
def http_method():
    if current_user.is_authenticated:
        form = HttpMethod()
        url = ""
        method = "get"
        cookie = {}
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.87 Safari/537.36",
            # "":""
        }
        status = ""
        data = {}
        msg = ""
        if request.args.get('status'):
            status = request.args.get('status')
        if form.method.data and form.url.data :
            method = form.method.data
            url = form.url.data
            if form.cookies.data:
                tmp = form.cookies.data
                for i in tmp.split(";"):
                    cookie[i[:i.index('=')]] = i[i.index("=")+1:]
            if form.posts.data:
                tmp = form.posts.data
                for i in tmp.split("&"):
                    data[i[:i.index('=')]] = i[i.index("=")+1:]
        print(url, method, data)
        if status == "do" or status == "":
            show = "no"
        if status == "did":
            show = "yes"
            print(url,method,cookie)
            if method in ['get','post'] and url!="":
                import requests
                if method == 'get':
                    try:
                        req = requests.get(url,headers=headers,cookies=cookie)
                        if req.status_code == 200:
                            msg = "success"
                            data = req.text
                            if not os.path.exists("templates/appliacation/tmp.html"):
                                open("templates/appliacation/tmp.html", "a+").close()
                            open("templates/appliacation/tmp.html", "wb").write(req.content)
                        else:
                            msg = "[xjusec]:"+str(req.status_code)
                    except Exception as e:
                        msg = "[xjusec]:"+str(e)
                if method =="post":
                    try:
                        req = requests.post(url, headers=headers, cookies=cookie,data=data)
                        if req.status_code == 200:
                            msg = "success"
                            data = req.text
                            if not os.path.exists("templates/appliacation/tmp.html"):
                                open("templates/appliacation/tmp.html", "a+").close()
                            open("templates/appliacation/tmp.html", "wb").write(req.content)
                        else:
                            msg = "[xjsuec]:"+str(req.status_code)
                    except Exception as e:
                        msg = "[xjusec]:"+ str(e)

        return render_template('appliacation/http_method.html',form=form,show=show,data=data,msg=msg)
    else:
        return redirect(url_for('my_web.login'))

@XJUSEC.route('/tmp_http')
def tmp():
    data = open("templates/tmp.html",'rb').read().decode()
    return data


@XJUSEC.route('/payloads',methods=['GET','POST'])
def Payloads():
    if current_user.is_authenticated:
        payload_lists_1 = os.listdir("./application/payload")
        payload_lists_2 = []
        form = NamePayload()
        if form.name.data:
            for i in payload_lists_1:
                if form.name.data in i:
                    payload_lists_2.append(i)
            return render_template('appliacation/payloads.html',lists=payload_lists_2,form=form)
        else:           
        # print(payload_lists)
            return render_template('appliacation/payloads.html',lists=payload_lists_1,form=form)
    else:
        return redirect(url_for('my_web.login'))
@XJUSEC.route('/payloadDetail/<payload>',methods=['GET','POST'])
def GetPayload(payload):
    if current_user.is_authenticated:
        payload_data = html.escape(open("./application/payload/{}".format(payload)).read())
        return payload_data
    else:
        return redirect(url_for('my_web.login'))
@XJUSEC.route('/getinfo')
def getinfo():
    data = {}
    load_data={}
    url = "null"
    ip ="null"
    cookie ="null"
    time = str(datetime.date.today())
    if request.args.get('url'):
        url  = request.args.get('url')
    if request.args.get('ip'):
        ip = request.args.get('ip')
    if request.args.get('cookie'):
        cookie = request.args.get('cookie')
    if request.args.get('time'):
        time = request.args.get('time')
    data['from_url'] = url
    data['ip'] = ip
    data['cookie'] = cookie
    data['time'] = time
    print(data)
    if safearg(url,ip,cookie):

        data_in_db = Xss(url=url,ip=ip,time=time,cookie=cookie)
        db.session.add(data_in_db)
        db.session.commit()
    mkdirlambda =lambda x: os.makedirs(x) if not os.path.exists(x) else True
    mkdirlambda(xss_data_path)
    json_file = xss_data_path+'/'+xss_data_name.format(datetime.date.today().strftime('%y%m%d'))
    if not os.path.exists(json_file):
        open(json_file,"a+").close()
    try:

        with open(json_file, "r",
                  encoding='utf-8') as file_r:
             try:
                load_data = json.load(file_r)
                num = len(load_data)
             except:
                num=0
             load_data[str(num + 1)] = data
             with open(json_file, "w",
                      encoding='utf-8') as file_w:
                 json.dump(load_data, file_w)
                 file_w.close()
             file_r.close()
        #！！！！！！
        return 'ok'
        # return redirect(url)
    except Exception as e:
        # return redirect(url)
        #！！！！！！
        return e