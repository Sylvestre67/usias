from django.db.models.signals import pre_save, post_save, m2m_changed, post_delete
from django.contrib.auth.models import Group
from models import User,Proposal
from django.dispatch import receiver

from guardian.shortcuts import assign_perm
import usias.settings as settings

@receiver(post_save, sender= Proposal)
def proposal_post_save(sender, instance, created, **kwargs):
	"""
	Add object level view permission to author of the proposal.
	"""
	proposal = instance
	if not proposal.author.has_perm('view_proposal', proposal) \
			and proposal.author != proposal.author.is_anonymous():
		assign_perm('view_proposal', proposal.author, proposal)
