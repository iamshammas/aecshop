from .models import *
from .views import *

def count(request):
    if 'admin' in request.path:
        return {}
    else:
        customer_id = c_id(request)
        if customer_id is None:
            return dict(itc=0)
        try:
            ct = cartlist.objects.filter(cart_id=customer_id).first()
            if ct is None:
                return dict(itc=0)
            cti = items.objects.filter(cart=ct)
            item_count = sum(c.qty for c in cti)
        except Exception as e:
            # Log the exception or handle it as needed
            return dict(itc=0)
        return dict(itc=item_count)