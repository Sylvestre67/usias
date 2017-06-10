from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.contrib.auth.models import Group
from models import User

import requests


