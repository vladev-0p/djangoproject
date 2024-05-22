from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from product.models import Product


# Create your views here.
@login_required
def index(request):
    products = Product.objects.filter(created_by=request.user)
    return render(request, 'dashboard/index.html',
                  {'products': products
                   })



