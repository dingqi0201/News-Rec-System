"""
    __init__.py
    ~~~~~~~~
    数据校验基类

    2020/9/2
"""
import re

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import StopValidation

from .csrf import CSRFProtect
from ..conf import get_conf_json
from ..libs.exceptions import APIParameterError, MsgException
from ..libs.helper import get_int, is_accept_json, get_plain_text, get_round

csrf = CSRFProtect()


class ZHTranslations(object):
    """翻译内置错误消息"""

    def __init__(self):
        self.messages = get_conf_json('i18n', 'forms-message')

    def gettext(self, string):
        return self.messages.get(string, string)

    def ngettext(self, singular, plural, n):
        return singular if n == 1 else plural


class BaseForm(FlaskForm):
    """自定义消息翻译和验证器返回类型"""

    class Meta(FlaskForm.Meta):
        def get_translations(self, form):
            return ZHTranslations()

    def check(self):
        """
        验证失败时抛出异常

        e.g.::

            # for POST, PUT, PATCH, DELETE: application/x-www-form-urlencoded, multipart/form-data
            # for JSON (POST, PUT, PATCH, DELETE): application/json
            # formdata=_Auto, likeness: validate_on_submit()
            # wrap_formdata: request.files, request.form, request.get_json()
            form = ASNAddForm().check()

            # for GET
            # ?ff=ok&asn=777
            form = ASNSearchForm(request.args).check()
            print(form.asn.data)

            # for custom data: MultiDict({'asn': 777})
            from werkzeug.datastructures import MultiDict
            my_data = MultiDict([('asn', 777)])
            form = ASNSearchForm(my_data).check()
            print(form.asn.data)

        :return:
        """
        valid = super(BaseForm, self).validate()
        if not valid:
            # form errors
            if is_accept_json():
                raise APIParameterError(self.errors)
            raise MsgException(self.errors)

        # 清除 csrf 字段
        if hasattr(self, 'csrf_token'):
            del self.csrf_token

        return self


class StripString:
    """DataRequired + 去除首尾空白赋值(或清除HTML标签)"""

    def __init__(self, message=None, allow_none=False, plain_text=False, cls_whitespace=False):
        self.message = message
        self.allow_none = allow_none
        self.plain_text = plain_text
        self.cls_whitespace = cls_whitespace

    def __call__(self, form, field):
        """
        e.g.::

            class SpecialRouteSearchForm(BaseForm):
                special_route = StringField('可为空, 空格, 去除首尾空白赋值', validators=[StripString(allow_none=True)])

            class SpecialRouteForm(BaseForm):
                special_route = StringField('必填, 去除首尾空白赋值', validators=[StripString()])

        """
        fdata = field.data
        if isinstance(fdata, str):
            if self.plain_text:
                fdata = get_plain_text(fdata)
            else:
                fdata = fdata.strip()
        if fdata == '' and not self.allow_none:
            if self.message is None:
                self.message = '{}不能为空{}'.format(field.label.text, '(纯文本)' if self.plain_text else '')
            raise StopValidation(self.message)
        getattr(form, field.name).data = re.sub(r'\s+', '', fdata) if self.cls_whitespace else fdata


class PositiveInteger:
    """DataRequired + 正整数赋值"""

    def __init__(self, message=None, allow_0=False, allow_none=False):
        self.message = message
        self.allow_0 = allow_0
        self.allow_none = allow_none

    def __call__(self, form, field):
        """
        e.g.::

            class ASNSearchForm(BaseForm):
                asn = StringField('可为空, 空格, 此外必须为正整数', validators=[PositiveInteger(allow_none=True)])

            class ASNForm(BaseForm):
                asn = StringField('必填正整数并转换后赋值', validators=[PositiveInteger()])

        """
        data = field.data.strip() if isinstance(field.data, str) else field.data
        fdata = get_int(data)
        if not ((data == '' or data is None) and self.allow_none) and (
                fdata is None or fdata < 1 and not (self.allow_0 and fdata == 0)):
            if self.message is None:
                self.message = '{}错误(非正整数{})'.format(field.label.text, '或0' if self.allow_0 else '')
            raise StopValidation(self.message)
        getattr(form, field.name).data = fdata


class FloatRound:
    """DataRequired + 浮点数赋值, 可指定小数位数"""

    def __init__(self, message=None, allow_none=False, allow_0=False, allow_lt0=False, precision=2):
        self.message = message
        self.allow_none = allow_none
        self.allow_0 = allow_0
        self.allow_lt0 = allow_lt0
        self.precision = precision

    def __call__(self, form, field):
        """
        e.g.::

            class BWPeakForm(BaseForm):
                bw_peak = FloatField('保留2位小数', validators=[FloatRound()])

        """
        data = field.data.strip() if isinstance(field.data, str) else field.data
        fdata = get_round(data, precision=self.precision)
        if (data == '' or data is None) and self.allow_none or (
                fdata is not None and (fdata > 0 or self.allow_lt0 and fdata < 0 or self.allow_0 and fdata == 0.0)):
            getattr(form, field.name).data = fdata
        else:
            if self.message is None:
                self.message = '{}(错误的浮点数)'.format(field.label.text)
            raise StopValidation(self.message)


class PagesForm(BaseForm):
    """后端分页"""
    page = StringField('页码', default=1, validators=[PositiveInteger(allow_none=True)])
    limit = StringField('每页记录数', default=60, validators=[PositiveInteger(allow_none=True)])
    count = StringField('总记录数', default=0, validators=[PositiveInteger(allow_none=True, allow_0=True)])
