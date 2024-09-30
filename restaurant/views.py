from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime, timedelta
import time
import random


daily_specials = [
    "Iskender Kebab",
    "Adana Kebab",
]


def main(request):
    template_name = "restaurant/main.html"

    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template
    return render(request, template_name, context)

def order(request):
    template_name = "restaurant/order.html"

    selected_dish = random.choice(daily_specials)

    context = {
        'current_time': time.ctime(),
        'selected_dish': selected_dish,
    }

    # delegate response to the template
    return render(request, template_name, context)


#Handle the form submission. Read out the form data. Generate a response.
def confirmation(request):
    '''
    Handle the form submission. 
    Read out the form data. 
    Generate a response.
    '''
    template_name = 'restaurant/confirmation.html'
    # print(request)

    # Get the current time and add 30 minutes
    current_time = datetime.now()
    ready_time = current_time + timedelta(minutes=30)
    # Format the ready time as "HH:MM AM/PM"
    ready_time_formatted = ready_time.strftime('%I:%M %p')
    
    # check if the request is a POST (vs GET)
    if request.POST:

        menu_items = [
            {'name': 'Lahmacun', 'price': 8.00, 'field': 'Lahmacun'},
            {'name': 'Doner (Gyro) Wrap', 'price': 15.00, 'field': 'Doner'},
            {'name': 'Istanbul Salad', 'price': 10.50, 'field': 'IstanbulSalad'},
            {'name': 'Pide', 'price': 17.00, 'field': 'Pide', 'options': {
                'cheese': 0, 'sucuk': 2.00, 'beef': 3.00
            }},
            {'name': 'Today\'s Special', 'price': 22.00, 'field': 'specialDish'}
        ]

        # Initialize total price
        total_price = 0
        selected_items = []

        # Loop through the menu items to check what was selected
        for item in menu_items:
            if request.POST.get(item['field']):
                selected_items.append(item)
                total_price += item['price']

                # If Pide has an option selected and add the option price
                if item['field'] == 'Pide':
                    pide_option = request.POST.get('pide_option')
                    if pide_option and pide_option in item['options']:
                        total_price += item['options'][pide_option]
                        selected_items[-1]['pide_option'] = pide_option
                        selected_items[-1]['pide_option_price'] = item['options'][pide_option]  # Store the price of the option

        # Retrieve customer information
        customer_name = request.POST.get('name')
        customer_phone = request.POST.get('phone')
        customer_email = request.POST.get('email')
        special_instructions = request.POST.get('special_instructions')

        # Prepare context with the data to pass to the confirmation page
        context = {
            'selected_items': selected_items,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'total_price': total_price,
            'ready_time': ready_time_formatted,
        }

        # generate a response
        return render(request, template_name, context)
    else:
        # if the client got here by making a GET on this URL, send back the form
        return redirect("order")

