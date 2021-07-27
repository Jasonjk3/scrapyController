from application.api_v1.model.project import Project
from application.base import log, ajaxResponse
from application.base.httpException import ServerError
from application.base.upload import save_file
from application.base import mysql_db as db
from datetime import datetime

def getProjectsList():
    try:
        models = Project.query.all()
        datas = []
        for model in models:
            data = {
                'project_id': model.project_id,
                'scrapy_id': model.scrapy_id,
                'scrapy_version': model.scrapy_version,
                'project_name': model.project_name,
                'create_time': model.create_time,
                'edit_time': model.edit_time,
                'note': model.note,
                'status': model.status,
            }
            datas.append(data)
        return ajaxResponse.success(message="成功",data=datas)
    except Exception as e:
        log.error("错误 - {}".format(e))
        raise ServerError()


def getProject(form):
    try:

        model = Project.query.filter_by(project_id=form.project_id.data).first()
        if model is None:
            return ajaxResponse.fail('project不存在')
        data = {
            'project_id': model.project_id,
            'scrapy_id': model.scrapy_id,
            'scrapy_version': model.scrapy_version,
            'project_name': model.project_name,
            'create_time': model.create_time,
            'edit_time': model.edit_time,
            'note': model.note,
            'status': model.status,
        }

        return ajaxResponse.success(message="成功",data=data)
    except Exception as e:
        log.error("错误 - {}".format(e))
        raise ServerError()


def addProject(form):
    try:
        hasName = Project.query.filter_by(project_name=form.project_name.data).first()
        if hasName:
            return ajaxResponse.fail(message='project_name 已存在，请更换')

        model = Project()
        model.project_name = form.project_name.data
        model.create_time= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.edit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        model.note = form.note.data
        model.status = 0

        db.session.add(model)
        db.session.commit()
        return ajaxResponse.success(message="成功")
    except Exception as e:
        log.error("错误 - {}".format(e))
        db.session.rollback()
        raise ServerError()

def uploadFile(file):
    try:
        path = save_file(file)

        return ajaxResponse.success(message="成功")
    except Exception as e:
        log.error("错误 - {}".format(e))
        raise ServerError()


def deleteProject(form):
    try:
        model = Project.query.filter_by(project_id=form.project_id.data).first()
        if model is None:
            return ajaxResponse.fail(message='project_id 不存在，请更换')
        db.session.delete(model)
        db.session.commit()
        # TODO  删除project的时候 一起删除爬虫
        return ajaxResponse.success(message="成功")
    except Exception as e:
        log.error("错误 - {}".format(e))
        raise ServerError()


def editProject(form):
    try:
        model = Project.query.filter_by(project_id=form.project_id.data).first()
        if model is None:
            return ajaxResponse.fail(message='project_id 不存在，请更换')

        if form.project_name.data:
            model.project_name = form.project_name.data

        if form.note.data:
            model.note = form.note.data
        model.edit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.session.commit()
        return ajaxResponse.success(message="成功")
    except Exception as e:
        log.error("错误 - {}".format(e))
        raise ServerError()

