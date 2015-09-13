from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import QueryDict
from lablackey.utils import get_or_none

from course.utils import get_or_create_student
from .models import UserMembership, Status, Subscription, Membership, Product
from user.models import User

from paypal.standard.ipn.signals import payment_was_successful, subscription_signup

@receiver(post_save,sender=User)
def post_save_user_handler(sender, **kwargs):
  user = kwargs['instance']
  UserMembership.objects.get_or_create(user=user)

_duid2='membership.listners.handle_successful_membership_payment'
@receiver(payment_was_successful, dispatch_uid=_duid2)
def handle_successful_membership_payment(sender,**kwargs):
  if sender.txn_type != "subscr_payment":
    return # not a membership payment
  if Status.objects.filter(transaction_id=sender.txn_id):
    return # This has already been processed
  params = QueryDict(sender.query)
  subscr_id=params.get('subscr_id',None)
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=subscr_id)
  subscription = get_or_none(Subscription,subscr_id=subscr_id)
  if not 'mc_gross' in params:
    mail_admins("Bad IPN","no mc_gross in txn %s"%sender.txn_id)
    return
  amt = params['mc_gross']
  if not subscription:
    try:
      membership = Membership.objects.get(name=params.get('option_name1',''))
    except Membership.DoesNotExist:
      b = "Could not find membership %s for txn %s"%(params.get('option_name1',''),sender.txn_id)
      mail_admins("Bad IPN",b)
      return
    try:
      product = Product.objects.get(unit_price=amt,membership=membership)
    except Product.DoesNotExist:
      b = "Could not find membership product %s $%s for txn %s"
      mail_admins("Bad IPN",b%(membership,amt,sender.txn_id))
      return
  Status.objects.create(
    subscription=subscription,
    paypalipn=sender,
    payment_method='paypal',
    amount=amt,
  )

_duid2='membership.listners.handle_subscription_signup'
@receiver(subscription_signup, dispatch_uid=_duid2)
def handle_subscription_signup(sender,**kwargs):
  params = QueryDict(sender.query)
  if sender.txn_type != "subscr_payment":
    return # not a membership payment
  if Subscription.objects.filter(subscr_id=params.get('subscr_id')):
    return # This has already been processed
  user,new_user = get_or_create_student(sender.payer_email,subscr_id=params.get('subscr_id',None))
  try:
    membership = Membership.objects.get(name=params.get('option_name1',''))
  except Membership.DoesNotExist:
    b = "Could not find membership %s for txn %s"%(params.get('option_name1',''),sender.txn_id)
    mail_admins("Bad IPN",b)
    return
  """Subscription(
    membership=membership"""
