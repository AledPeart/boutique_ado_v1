from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages 
from django.db.models import Q #allows us to serch with 'or' logic as well as 'and'
from .models import Product, Category
from django.db.models.functions import Lower
from .forms import ProductForm

# Create your views here.

def all_products(request):
    """ A view to show all products, including sorting and search queries """

    products = Product.objects.all()
    query = None #this is to ensure that error not thrown if search query=blank
    categories = None
    sort = None
    direction = None

    if request.GET: #GET method passed in to the url

        #NB __ syntax allows us to look for the 'name' field in the category model
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}' #reverses the sort direction
            products = products.order_by(sortkey)


        if 'category' in request.GET: 
            categories = request.GET['category'].split(',') #splits the categories into a list at the commas
            products = products.filter(category__name__in=categories) #filters all products to just those in the list
            categories = Category.objects.filter(name__in=categories) #filters all categories to those searched by user

        if 'q' in request.GET: #q is the name of our text input
            query = request.GET['q']
            if not query: #if a blank query submitterd
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products')) #return user to products url

            queries = Q(name__icontains=query) | Q(description__icontains=query)
            #Q object where name OR description is in the query (|=or, i=case insensitive)
            products = products.filter(queries) #filter method to filter the queries

    current_sorting = f'{sort}_{direction}'

      
    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """

    product = get_object_or_404(Product, pk=product_id)

    context = {
        'product': product,
    }

    return render(request, 'products/product_detail.html', context)


def add_product(request):
    """ Add a product to the store """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)


def edit_product(request, product_id):
    """ Edit a product in the store """
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure the form is valid.')
    else:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)


def delete_product(request, product_id):
    """ Delete a product from the store """
    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))