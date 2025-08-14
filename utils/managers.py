from datetime import datetime

from django.db import models

class ActiveManager(models.Manager):
    """ Менеджер контролирует что бы пользователю выводились только актуальные объявления """
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)

