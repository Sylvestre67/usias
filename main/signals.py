from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.contrib.auth.models import Group
from models import User,Proposal
from django.dispatch import receiver
import logging

from guardian.shortcuts import assign_perm
from guardian.core import ObjectPermissionChecker
import usias.settings as settings

@receiver(post_save, sender= Proposal)
def proposal_post_save(sender, instance, created, **kwargs):
	"""
	Add object level view permission to author of the proposal, and Admin/Board teams.
	"""
	proposal = instance
	if created:
		admin_group = assign_perm_to_group(instance,'admin','view_proposal')
		board_group = assign_perm_to_group(instance,'board','view_proposal')

	if not proposal.author.has_perm('view_proposal', proposal) \
			and proposal.author != proposal.author.is_anonymous():
		assign_perm('view_proposal', proposal.author, proposal)


def assign_perm_to_group(instance,name,permissioin):
	"""
	Assign a Object Level Permission for instance to a group.
	:param instance: django.Object
	:param name: Str
	:param perm: Str
	:return: django.Object
	"""
	logger = logging.getLogger(__name__)

	try:
		group = Group.objects.get(name=name)
		assign_perm(permissioin, group, instance)
	except Exception as e:
		logger.exception(e)

	return instance
