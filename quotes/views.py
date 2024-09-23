from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

quotes = [
    "A nation that does not know its past has no future..",
    "Everything we see in the world is the creative work of women.",
    "The biggest war is the war against ignorance",
    "Do not be afraid of telling the truth.",
    "If a nation is artless, it means that one of its lifelines is cut off.",
    "Educate the youth. Give them the positive ideas of lore and science. You will meet the brightness of the future with them."
]

images = [
    "/static/img1.jpg", 
    "/static/img2.jpg",
    "/static/img3.jpg",
    "/static/img4.jpg"
]

def main_page(request):
    '''
    A function to respond to the / URL.
    This function selects a random quote and image, then delegates work to the HTML template.
    '''
    # this template will present the response
    template_name = "quotes/quote.html"

    # select a random quote and image
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)

    # create a dictionary of context variables
    context = {
        'quote': selected_quote,
        'image': selected_image,
    }

    # delegate response to the template
    return render(request, template_name, context)


def quote(request):
    '''
    A function to respond to the /quote URL.
    This function selects a random quote and image, then delegates work to the HTML template.
    '''
    # this template will present the response
    template_name = "quotes/quote.html"

    # select a random quote and image
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)

    # create a dictionary of context variables
    context = {
        'quote': selected_quote,
        'image': selected_image,
    }

    # delegate response to the template
    return render(request, template_name, context)


def show_all(request):
    '''
    A function to respond to the /show_all URL.
    This function passes all quotes and images to the HTML template.
    '''
    # this template will present the response
    template_name = "quotes/show_all.html"

    # create a dictionary of context variables
    context = {
        'quotes': quotes,
        'images': images,
    }

    # delegate response to the template
    return render(request, template_name, context)

def about(request):

    template_name = "quotes/about.html"

    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template
    return render(request, template_name, context)
