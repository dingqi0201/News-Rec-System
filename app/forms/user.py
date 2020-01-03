"""
    user.py
    ~~~~~~~~
    views.user 数据校验

    :author: Fufu, 2019/9/21
"""
from flask import current_app
from flask_login import current_user
from wtforms import StringField, IntegerField
from wtforms.validators import ValidationError, Email

from . import BaseForm, StripString, PositiveInteger
from ..models.user import TBUser, TBRole


class UserSearchForm(BaseForm):
    job_number = StringField('工号', validators=[PositiveInteger(allow_none=True)])
    realname = StringField('姓名', validators=[StripString(allow_none=True)])


class UserJobNumberForm(BaseForm):
    job_number = StringField('工号', validators=[PositiveInteger()])

    def validate_job_number(self, field):
        if not TBUser.query.filter_by(job_number=field.data).first():
            raise ValidationError('工号{}不存在'.format(field.data))


class UserAuthorizeForm(UserJobNumberForm):
    id = IntegerField('ID', validators=[PositiveInteger()])
    role_id = StringField('权限组', validators=[PositiveInteger()])
    email = StringField('邮箱', validators=[StripString(), Email()])
    status = StringField('状态', default=1, validators=[PositiveInteger()])

    def validate_role_id(self, field):
        if field.data == current_app.config.get('SYS_ROLE_ID', 0):
            raise ValidationError('禁止授权到该权限组')
        if not TBRole.query.get(field.data):
            raise ValidationError('权限组{}不存在'.format(field.data))

    def validate_job_number(self, field):
        if current_user.job_number == field.data:
            raise ValidationError('无法修改自己权限组')
