from  flask import render_template,Blueprint,redirect,url_for,flash,request,session
from flask_login import LoginManager,login_user,UserMixin,logout_user,login_required,current_user
from awd.admin.Form import Control__off
from awd.admin.config import *
from awd.admin.AWDInfoDb import AWDInfo,db
import os
AWD=Blueprint('my_awd',__name__)

@AWD.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('awd/admin/index.html')
    else:
        return redirect(url_for('my_web.login'))
        # return redirect(url_for('my_web.login'))
@AWD.route('/teams')
def teams():
    if current_user.is_authenticated:
        return render_template('awd/admin/teams.html')
    else:
        return redirect(url_for('my_web.login'))
@AWD.route('/create',methods=['GET','POST'])
def create():
    if current_user.is_authenticated:
        form = Control__off()
        msg =""
        return render_template('awd/admin/create.html',formoff=form,msg=msg)
    else:
        return redirect(url_for('my_web.login'))

@AWD.route('/control')
def control():
    data = {}
    datas = AWDInfo.query.order_by(AWDInfo.Id.desc()).all()
    for i in datas:
        tmp ={}
        tmp['num'] = len(data)+1
        tmp['teamnum'] = i.teamnum
        tmp['dockernum'] = i.dockernum
        tmp["dockerimages_webdirs"] = i.dockerimages_webdirs
        tmp['time'] = i.time
        tmp['id'] = i.Id
        data[str(len(data)+1)] = tmp
    id_list = []
    for i in range(int(len(data))):
        id_list.append(i+1)

    return  render_template('awd/admin/control.html',data=data,id_list=id_list)

@AWD.route('/configs')
def configs():
    if current_user.is_authenticated:
        return render_template('awd/admin/configs.html')
    else:
        return redirect(url_for('my_web.login'))


@AWD.route('/do',methods=['GET','POST'])
def do():
    form = Control__off()
    if form.teamnum.data and form.dockerimages_webdirs.data:
        teamnum = form.teamnum.data
        dockernum = form.dockernum.data
        dockerimages_webdirs = form.dockerimages_webdirs.data
        # webdirs = form.webdirs.data
        time = form.time.data
        if len(dockerimages_webdirs.split(";")) != int(dockernum):
            msg = "[xjusec]:docker数与docker镜像不匹配！"
            return render_template('awd/admin/create.html', formoff=form,msg = msg)
        for i in dockerimages_webdirs.split(";"):
            if os.path.exists(webdirpath+i.split(":")[1]):
                pass
            else:
                msg = "[xjusec]:{}文件夹不存在！".format(i.split(":")[1])
                return render_template('awd/admin/create.html', formoff=form, msg=msg)
        print(teamnum,dockernum,dockerimages_webdirs,time)
        info = AWDInfo(teamnum=teamnum,dockerimages_webdirs=dockerimages_webdirs,dockernum=dockernum,time=time)
        db.session.add(info)
        db.session.commit()
        return redirect(url_for("my_awd.control"))
    else:
        return render_template('hack.html')


@AWD.route('/manage')
def manage():
    if request.args.get('id'):
        return