from django.shortcuts import render, redirect

# Create your views here.

def view_bag(request):
    """ A view to return the bag contents page """
    
    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """Add a quantity of the specified product to the shopping bag"""

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    # This is where users goods will be kept. session means the info is held in 
    # the http session while the user is still browsing the site
    # this checks if the variable 'bag' exists and if not creates one, the empty dict is where the items eill be stored
    bag = request.session.get('bag', {})

    # creates a 'key' of the items id and sets it equal to the quantity of items
    # if an items is already in the bag it is incremented accordingly
    if item_id in list(bag.keys()):
        bag[item_id] += quantity
    else:
        bag[item_id] = quantity

    request.session['bag'] = bag
    return redirect(redirect_url)
