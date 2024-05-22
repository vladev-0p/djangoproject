from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from product.forms import NewProductForm, EditProductForm
from product.models import Product, Category


def browse(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(is_sold=False)
    category_id = request.GET.get('category', 0)
    categories = Category.objects.all()

    if category_id:
        products = products.filter(category_id=category_id)
    if query:
        products = products.filter(name__icontains=query)
    return render(request, 'product/browse.html',
                  {'products': products,
                   'query': query,
                   'categories': categories,
                   'category_id': int(category_id),
                   })


# Create your views here.
def detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related_products = Product.objects.filter(category=product.category, is_sold=False).exclude(pk=pk)[0:3]
    return render(request, 'product/detail.html',
                  {'product': product,
                   'related_products': related_products,
                   })


@login_required
def new_product(request):
    if request.method == 'POST':
        form = NewProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = NewProductForm()
    return render(request, 'product/product.html',
                  {
                      'form': form,
                      'title': 'New product',
                  })


@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    product.delete()

    return redirect('dashboard:index')


@login_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.save()
            return redirect('product:detail', pk=product.id)
    else:
        form = EditProductForm(instance=product)
    return render(request, 'product/product.html',
                  {
                      'form': form,
                      'title': 'Edit product',
                  })
