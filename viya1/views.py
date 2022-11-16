

from django.shortcuts import render

from viya1.models import Property, ClientDocuments, Client, FamilyMember


def about(request):
    # header
    property = Property.objects.all().order_by('-created_on')

    context = {
        'property': property,
    }
    print(context)
    return render(request, 'admin/', context)



from django.shortcuts import render

from django.shortcuts import render
import json
# Create your views here.
def indexview(request):
    city=City.objects.all().order_by('name')
    city_list=list(city.values('name','id'))
    city_list=json.dumps(city_list)

    division=Division.objects.all().order_by('name')
    division_list=list(division.values('name','city__name','id'))
    division_list=json.dumps(division_list)

    district=District.objects.all().order_by('name')
    district_list=list(district.values('name','division__name','id'))
    district_list=json.dumps(district_list)

    subdistrict=SubDistrict.objects.all().order_by('name')
    subdistrict_list=list(subdistrict.values('name','district__name','id'))
    subdistrict_list=json.dumps(subdistrict_list)

    context={
        "city_list":city_list,
        "division_list":division_list,
        "district_list":district_list,
        "subdistrict_list":subdistrict_list,
    }
    # return render(request, 'index.html', context)
    return render(request, 'admin/', context)




from .models import Contact, City, Division, District, SubDistrict

from .serializers import ContactSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
class ContactListCreateAPIView(ListCreateAPIView):
    serializer_class=ContactSerializer
    queryset=Contact.objects.all()
class ContactRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class=ContactSerializer
    queryset=Contact.objects.all()
    lookup_field='id'


from django.shortcuts import render
from django.http import HttpResponse
from viya1.functions import handle_uploaded_file
from viya1.forms import ClientDocumentsForm


def index(request, slug):
    slug_1 = Client.objects.get(slug1=slug)
    members = FamilyMember.objects.get(client_key= slug_1.id)
    print(members)

    if request.method == 'POST':

        context = {
            'members': members,
            # 'posts': posts,
        }
        print(context)
        student = ClientDocuments(request.POST, request.FILES)
        if student.is_valid():
            handle_uploaded_file(request.FILES['file'])
            model_instance = student.save(commit=False)
            model_instance.save()
            return render(request, 'admin/', context)
            # return HttpResponse("File uploaded successfuly")  /admin

    else:
        context = {
            'members': members,
            # 'posts': posts,
        }
        print(context)
        student = ClientDocuments()
        return render(request, 'admin/viya1/client/profil.html', context)
