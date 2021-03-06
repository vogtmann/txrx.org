from django.conf.urls import url
from django.contrib.auth.decorators import user_passes_test
import lablackey.views

from django.http.response import JsonResponse
from django.template.response import TemplateResponse
from djstripe.models import Transfer
from drop.models import Order
from drop.giftcard.models import GiftCardProduct
from store.models import Consumable, CourseCheckout
from course.models import SessionProduct

import json

@user_passes_test(lambda u: u.is_superuser)
def transfers(request):
  transfers = []
  classes = (SessionProduct,Consumable,CourseCheckout,GiftCardProduct)
  for transfer in Transfer.objects.all():
    totals = {c:0 for c in classes}
    for charge in transfer.charge_set.all():
      charge_total = charge.amount - charge.fee
      if not 'order_id' in charge.metadata:
        continue
      order = Order.objects.get(pk=charge.metadata['order_id'])
      for item in order.items.all():
        item_ratio = item.line_total / order.order_total
        if isinstance(item.product,classes):
          totals[item.product.__class__] += item_ratio*charge_total
        else:
          print item.product.__class__,transfer.stripe_id
    _totals = [totals[c] for c in classes]
    transfers.append((transfer,_totals,transfer.amount-sum(_totals)))
  sums = [0,0,0,0]
  for transfer,totals,error in transfers:
    for i,t in enumerate(totals):
      sums[i] += t
  values = {
    'transfers': transfers,
    'transfers_completed': json.dumps({ t.stripe_id: t.metadata.get("completed",None) for t in Transfer.objects.all()}),
    'labels': ["transfer","transfer.total (error)","classes","consumables","checkouts","giftcards"],
    'sums': sums,
  }
  return TemplateResponse(request,"txrx/transfers.html",values)

@user_passes_test(lambda u: u.is_superuser)
def complete_transfer(request,stripe_id):
  t = Transfer.objects.get(stripe_id=stripe_id)
  t.metadata['completed'] = not t.metadata.get('completed',None)
  t.save()
  return JsonResponse({'completed': t.metadata['completed']})

@user_passes_test(lambda u: u.is_superuser)
def user_zip(request):
  from redtape.models import Signature
  from collections import defaultdict
  aggregates = defaultdict(int)
  for s in Signature.objects.filter(document_id=3):
    aggregates[s.data['zip']] += 1
  values = {
    'zip_table': sorted(aggregates.items(),key=lambda i: -i[1]),
  }
  return TemplateResponse(request,'txrx/user_zip.html',values)

urlpatterns = [
  url(r'^work/$',lablackey.views.single_page_app),
  url(r'^txrx/transfers/$',transfers),
  url(r'^txrx/complete_transfer/([_\w\d]+)/$',complete_transfer),
  url(r'^support/$',lablackey.views.render_template,kwargs={'template': 'flatpages/support.html'}),
  url(r'^crafters-for-good/$',lablackey.views.render_template,kwargs={'template': 'crafters/index.html'}),
  url(r'^crafters-for-good/makeathons/$',lablackey.views.render_template,kwargs={'template': 'crafters/makeathons.html'}),
  url(r'^crafters-for-good/seminars/$',lablackey.views.render_template,kwargs={'template': 'crafters/seminars.html'}),
  url(r'^user_zip/$',user_zip),
]
