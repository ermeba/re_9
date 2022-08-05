from django.shortcuts import render
from django.shortcuts import render
# from taggit.models import Tag
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from .forms import OrderForm
# Create your views here.
from viya1.models import Property


def about(request):
    # header
    property = Property.objects.all().order_by('-created_date')

    context = {
        'property': property,
    }
    return render(request, 'index.html', context)