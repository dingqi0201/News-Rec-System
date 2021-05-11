"""
    role.py
    ~~~~~~~~
    views.role 数据校验

    2020/12/5
"""
from wtforms import StringField
from wtforms.validators import ValidationError

from . import BaseForm, StripString, PositiveInteger
from ..models.user import TBRole


class RoleSearchForm(BaseForm):
    role = StringField('权限标识', validators=[StripString(plain_text=True, allow_none=True)])


class RoleDeleteForm(BaseForm):
    role_id = StringField('权限ID', validators=[PositiveInteger()])

    def validate_role_id(self, field):
        if not TBRole.query.get(field.data):
            raise ValidationError('权限组异常, 无法删除')


class RoleAddEditForm(BaseForm):
    role = StringField('权限标识', validators=[StripString(plain_text=True)])
    role_id = StringField('权限ID', validators=[PositiveInteger(allow_0=True)])
    role_name = StringField('权限名称', validators=[StripString(plain_text=True)])
    role_allow = StringField('允许权限', validators=[StripString(plain_text=True, cls_whitespace=True)])
    role_deny = StringField('禁止权限', validators=[StripString(plain_text=True, allow_none=True, cls_whitespace=True)])

    def validate_role_id(self, field):
        if TBRole.query.filter(TBRole.role == self.role.data, TBRole.role_id != field.data).first():
            raise ValidationError('权限标识{}已存在'.format(self.role.data))

    def validate_role_deny(self, field):
        if field.data and not all(['.' in x for x in field.data.split(',')]):
            raise ValidationError('禁止权限必须是视图函数级别')
