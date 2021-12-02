from django.db import models
from django.forms.models import model_to_dict

ENV_ITEMS = [
    ('dev', 'dev开发环境'), ('uat', 'uat测试环境'), ('pre', 'pre预发环境'), ('aliprod', '生产环境')
]


class CommonModel(models.Model):
    created_at = models.DateTimeField(null=True, blank=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField( null=True, blank=True, auto_now=True, verbose_name='创建时间')
    created_by = models.UUIDField(null=True, blank=True, verbose_name='创建者')
    updated_by = models.UUIDField(null=True, blank=True, verbose_name='更新者')

    class Meta:
        abstract = True


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self.__initial = self._dict

    @property
    def diff(self):
        d1 = self.__initial
        d2 = self._dict
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        return bool(self.diff)

    @property
    def changed_fields(self):
        return self.diff.keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._dict

    @property
    def _dict(self):
        return model_to_dict(self, fields=[field.name for field in
                                           self._meta.fields])
