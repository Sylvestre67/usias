# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
import uuid

from django.contrib.postgres.fields import JSONField

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin, Group
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

from django.utils import timezone
from django_extensions.db.models import TimeStampedModel

class UserManager(BaseUserManager):

	def _create_user(self, email, password, is_staff, is_superuser, **extra):
		if not email:
			raise ValueError('Email is required')
		now = timezone.now()
		email = self.normalize_email(email)
		user = self.model(
				email=email,
				is_staff=is_staff,
				is_active=True,
				is_superuser=is_superuser,
				last_login=now,
				date_joined=now,
				**extra
		)
		user.set_password(password)
		user.save(using=self._db)

		return user

	def create_user(self, email, password=None, **extra):
		return self._create_user(email, password, False, False, **extra)

	def create_superuser(self, email, password, **extra):
		return self._create_user(email, password, True, True, **extra)

class User(AbstractBaseUser, PermissionsMixin):
	date_joined      = models.DateTimeField(default=timezone.now)
	email            = models.EmailField(max_length=254, unique=True, blank=False)
	first_name       = models.CharField(max_length=32, blank=True)
	is_staff         = models.BooleanField(default=False)
	is_active        = models.BooleanField(default=True)
	last_name        = models.CharField(max_length=32, blank=True)
	phone_number     = models.CharField(max_length=32, blank=True)

	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def get_full_name(self):
		return ("%s %s" % (self.first_name, self.last_name)).strip()

	def get_short_name(self):
		return self.first_name

	def email_user(self, subject, message, from_email=None):
		send_mail(subject, message, from_email, [self.email])

	def get_absolute_url(self):
		return reverse('user_profile',args=[self.pk])

class UUIDModel(TimeStampedModel):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Proposal(UUIDModel):
	title = models.CharField(max_length=256, blank=True)
	author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

	class Meta:
		permissions = (
			('view_proposal', 'View proposal'),
		)
		verbose_name = 'proposal'
		verbose_name_plural = 'proposals'

	def __unicode__(self):
		return u'%s' % (self.title)