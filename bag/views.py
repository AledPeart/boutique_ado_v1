from django.shortcuts import render, redirect, reverse, HttpResponse
from django.contrib import messages

from products.models import Product 

# Create your views here.

def view_bag(request):
    """ A view to return the bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    #size is none initially but equal to the size if in the post request
    size = None 
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # This is where users goods will be kept. session means the info is held in 
    # the http session while the user is still browsing the site
    # this checks if the variable 'bag' exists and if not creates one, the empty dict is where the items eill be stored
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()): #if the item is in the bag 
            if size in bag[item_id]['items_by_size'].keys(): #is there another item of the same size and id?
                bag[item_id]['items_by_size'][size] += quantity #increment accordingly
            else:
                bag[item_id]['items_by_size'][size] = quantity #the item is there already, but this is a new size increment accordingly
        else: #if the item is not in the bag already we add it, but as a dictionary
              # as there may be items with the same id but different sizes
            bag[item_id] = {'items_by_size': {size: quantity}}
    else: #if there is no size:
    # creates a 'key' of the items id and sets it equal to the quantity of items
    # if an items is already in the bag it is incremented accordingly
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your bag')

    request.session['bag'] = bag
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust quantity of the specified products in the shopping bag"""
    quantity = int(request.POST.get('quantity'))
    #size is none initially but equal to the size if in the post request
    size = None 
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    # This is where users goods will be kept. session means the info is held in 
    # the http session while the user is still browsing the site
    # this checks if the variable 'bag' exists and if not creates one, the empty dict is where the items eill be stored
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
        else: 
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item.id) 
    
    else: 
        if quantity > 0:
            bag[item_id] = quantity
        else: 
            bag.pop[item_id]

    
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    try:
        #size is none initially but equal to the size if in the post request
        size = None 
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        # This is where users goods will be kept. session means the info is held in 
        # the http session while the user is still browsing the site
        # this checks if the variable 'bag' exists and if not creates one, the empty dict is where the items eill be stored
        bag = request.session.get('bag', {})

        if size:
                del bag[item_id]['items_by_size'][size]
                if not bag[item_id]['items_by_size']:
                    bag.pop(item.id) 
        
        else:  
            bag.pop(item_id)

        
        request.session['bag'] = bag
        return HttpResponse(status=200)
    except Exception as e:
        return HttpResponse(status=500)


    