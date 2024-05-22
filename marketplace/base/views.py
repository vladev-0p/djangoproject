from django.http import HttpResponse
from django.shortcuts import render, redirect

from base.forms import SignupForm
from product.models import Category, Product


# Create your views here.
def index(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_sold=False)[0:6]
    return render(request, 'base/index.html',
                  {
                      'products': products,
                      'categories': categories
                  }
                  )


def contact(request):
    return render(request, 'base/contact.html')


def signup(request):
    if request.method=='POST':
        form= SignupForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('/login')

    form = SignupForm()
    return render(request, 'base/signup.html',
                  {'form': form
                   })
