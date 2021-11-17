from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.db.models import Q #allows us to serch with 'or' logic as well as 'and'
from .models import Product

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None #this is to ensure that error not thrown if search query=blank

    if request.GET: #GEWT method passed in to the url
        if 'q' in request.GET: #q is the name of our text input
            query = request.GET['q']
            if not query: #if a blank query submitterd
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products')) #return user to products url

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            #Q object where name OR description is in the query (|=or, i=case insensitive)
            products = products.filter(queries) #filter method to filter the queries

             
    context = {
        'products': products,
        'search_term': query,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)
