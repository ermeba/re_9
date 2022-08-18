from django.contrib import admin
# from django.forms import forms
from django import forms
from django.contrib.admin import display
from django.contrib.sites import requests
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import path, include, reverse
from django.utils.html import format_html
from django.http import HttpResponse
from django_admin_listfilter_dropdown.filters import (DropdownFilter, ChoiceDropdownFilter, RelatedDropdownFilter,
                                                      RelatedOnlyDropdownFilter)
from admin_numeric_filter.admin import NumericFilterModelAdmin, SingleNumericFilter, RangeNumericFilter, \
    SliderNumericFilter
from rest_framework.generics import get_object_or_404

from viya1.functions import handle_uploaded_file
from viya1.models import City, Division, District, SubDistrict, Address, Type, Status, Property, Sours, PropertySingle, \
    Partner, Project, Client, ClientContact, FamilyMember, References, FamilyDocuments, ClientDocuments
from django.shortcuts import render

#Property, Type, Status, PropertySingle

import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
from time import sleep
from random import randint


# Adding Property, Status and Type tables to Admin


class StatusInline(admin.TabularInline):
    model = Status
    max_num = 1

    def has_delete_permission(self, request, obj=None):
        return False


class TypeInline(admin.TabularInline):
    model = Type
    max_num = 1

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False

class SoursInline(admin.TabularInline):
    model = Sours
    max_num = 1

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False

class PropertySingleInline(admin.TabularInline):
    model = PropertySingle
    extra = 5



class AddressInline(admin.TabularInline):
    model = Type
    max_num = 1

    class Media:
        js = ("viya1/selectajax.js",)

    def has_delete_permission(self, request, obj=None):
        return False

    # def has_add_permission(self, request, obj):
    #     return False

# templates/admin/viya1/adding_property/change_form.html

class ScrapData(forms.Form):
    scrap_data = forms.FileField()


class NameForm(forms.Form):
    get_link = forms.CharField(label='Your name', max_length=100)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/viya1/property/change_list.html'
    actions = ('make_offers_available',)
    inlines = [ StatusInline, TypeInline, SoursInline, PropertySingleInline]
    list_display = [ 'image_preview',
                     'offer',
                     'name',
                     # 'price_dollar',
                     'price',
                     'nr_of_rooms',
                     'brut_case_net',
                     'city_case_division',
                     # 'link',
                     'pdf1',
                     'edit',
                     'status']
    search_fields = ['offer', 'advert_no']
    list_editable = []
    list_display_links = ('image_preview', 'offer')
    list_per_page = 20

    list_filter = [
                   "name",
                   "nr_of_rooms",
                   ("city", RelatedOnlyDropdownFilter),
                   ("division", RelatedOnlyDropdownFilter),
                   ("price", RangeNumericFilter),
                   ("square_meter_brut", RangeNumericFilter),
                   'status',
                   'sours',
                   'created_on',
                   ]
    #
    # def xml(self, obj):
    #     return format_html('<input type="button" onclick="location.href="/admin/viya1/my_model/{}/change/" '
    #                        'value="xml" />'
    #                        , obj.id)

    @admin.display(description='PDF')
    def pdf1(self, obj):
        return format_html('<input type="button" onclick="window.open(`/media/{}`,`_blank`)"'
                           'value="pdf" />'
                           , obj.pdf)


    # onclick="window.location.href=`/media/{}`"
    def edit(self, obj):
        prop = Property.objects.all()
        return format_html('<input type="button" onclick="window.open(`/admin/viya1/property/{}/change/`,`_blank`)"'
                           'value="edit" />'
                           , obj.id)

    # def delete_button(self, obj):
    #     return format_html('<input type="button" onclick="location.href="/admin/viya1/my_model/{}/change/" '
    #                        'value="Delete" />'
    #                        , obj.id)

    # def delete(self, obj):
    #     view_name = "admin:{}_{}_delete".format(obj._meta.app_label, obj._meta.model_name)
    #     link = reverse(view_name, args=[property])
    #     html = '<input type="button" onclick="location.href=\'{}\'" value="Delete" />'.format(link)


    def make_offers_available(self, modeladmin, request, queryset):
        queryset.update(is_available=True)
    make_offers_available.short_description = "Mark selected offers as available"


    @admin.display(description='Location')
    def city_case_division(self, obj):
        return ("%s / %s" % (obj.city, obj.division))

    # @admin.display(description='Price in $')
    # def price_dollar(self, obj):
    #     return ("$ %s " % ( '{:,}'.format(obj.price)))

    @admin.display(description='Brut - Net m2')
    def brut_case_net(self, obj):
        return "%s - %sm2" % (obj.square_meter_brut, obj.square_meter_net)


    # def get_type_of_property(self, obj):
    #     return obj.type.type_of_property

    # @display(ordering='type_of_property', description='Type')
    # def get_type(self, obj):
    #     return obj.property.type_of_property

    # def status_of_property_n(self, obj):


    class Media:
        js = ("viya1/selectajax.js",)

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('scrap_data/', self.scrap_data),
            path('scrap_data/get_link/', self.get_link),
        ]

        return my_urls + urls

    def scrap_data(self, request):
        if request.method == "POST":
             link = 'jjj'
        #     csv_file = request.FILES["csv_file"]
        #     reader = csv.reader(csv_file)
        #
        #     self.message_user(request, "Your csv file has been imported")
        #     return redirect("..")
        form = ScrapData()
        data = {"form": form}
        print("data", data)
        return render(
            request,   "admin/viya1/property/csv_form.html", data
         )

    def get_link(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            form = NameForm(request.POST)
            # check whether it's valid:
            if form.is_valid():
                # process the data in form.cleaned_data as required
                # ...
                # redirect to a new URL:
                return HttpResponseRedirect('/thanks/')

        # if a GET (or any other method) we'll create a blank form
        else:
            form = NameForm()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # chromedriver_path = "C:\\Users\\Lenovo\\PycharmProjects\\viya\\chromedriver.exe"
        # service = Service(chromedriver_path)
        # driver = webdriver.Chrome(service=service)

        driver = webdriver.Chrome(options=chrome_options)



        url = "https://www.hepsiemlak.com/istanbul-kadikoy-suadiye-kiralik/daire/62823-5161"
        # url ='https://www.sahibinden.com/ilan/emlak-konut-satilik-agaoglu-my-towerland-atasehir-de-full-deniz-manzarali-3-plus1-1036362789/detay'
        driver.get(url)
        sleep(randint(3, 5))

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()

        links = soup.find_all("a")
        top10 = set()


        # soup = soup.find("body").find("ul")

        #    data = soup.find('div', class_="txt")
        for link in links:
            top10.add(link.get("href"))

        # for link in top10:
        #     print(link.text)

        import webbrowser

        print("Please enter the link")
        link = input()
        webbrowser.open(link)


        # We’ll make the program sleep for some small random number of seconds to ensure the
        # webpage loads and we don’t look too much like a bot
        # return render(request, "admin/viya1/property/scrap_result.html", {'form': form})
        return HttpResponse(top10)


# @admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/viya1/property/change_list.html'

    inlines = []
    list_display = ['name_of_company',  'year_of_establishment',  'address', 'phone_number', 'number_of_project',
                    'show_firm_url', 'image_preview']
    # search_fields = ['advert_no', 'city', 'division' ]
    # list_filter = ['nr_of_rooms', 'nr_of_bathrooms', 'city', 'division' ]
    list_editable = ['number_of_project']
    list_per_page = 25

    def show_firm_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.website)

admin.site.register(Partner, PartnerAdmin)


class ProjectAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/viya1/property/change_list.html'

    inlines = []
    list_display = ['project', 'name_of_project',  'year_of_completion', 'type_of_project',
                    'address', 'phone_number', 'show_firm_url', 'image_preview']
    # search_fields = ['advert_no', 'city', 'division' ]
    # list_filter = ['nr_of_rooms', 'nr_of_bathrooms', 'city', 'division' ]
    # list_editable = ['number_of_project']
    list_per_page = 25

    def show_firm_url(self, obj):
        return format_html("<a href='{url}'>{url}</a>", url=obj.website)

    # @admin.display(description='Completed on')
    # def completation_case_year(self, obj):
    #     return ("%s/%s" % (obj.status_of_project, obj.year_of_completion))

admin.site.register(Project, ProjectAdmin)


class ClientContactInline(admin.TabularInline):
    model = ClientContact
    extra = 1


class ClientDocumentsInline(admin.TabularInline):
    model = ClientDocuments
    extra = 1


class ReferencesInline(admin.TabularInline):
    model = References
    extra = 1
#
# class RelationshipsInline(admin.TabularInline):
#     model = Relationships
#     max_num = 1


class FamilyMemberInline(admin.TabularInline):
    model = FamilyMember
    extra = 1

class FamilyDocumentsInline(admin.TabularInline):
    model = FamilyDocuments
    extra = 1

class OpenProfile(forms.Form):
    open_profile = forms.FileField()

from django.shortcuts import render
from django.http import HttpResponse
from viya1.functions import handle_uploaded_file
from viya1.forms import ClientDocumentsForm

class ClientAdmin(admin.ModelAdmin):
    # change_list_template = 'admin/viya1/property/change_list.html'

    inlines = [ClientContactInline, ClientDocumentsInline, ReferencesInline,FamilyMemberInline,  FamilyDocumentsInline, ]
    list_display = ['image_preview', 'name','surname', 'birthday', 'address' , 'edit', 'profil']
    # search_fields = ['advert_no', 'city', 'division' ]
    # list_filter = ['nr_of_rooms', 'nr_of_bathrooms', 'city', 'division' ]
    # list_editable = ['number_of_project']
    list_per_page = 25

    # def show_firm_url(self, obj):
    #     return format_html("<a href='{url}'>{url}</a>", url=obj.website)

    # @admin.display(description='Completed on')
    # def completation_case_year(self, obj):
    #     return ("%s/%s" % (obj.status_of_project, obj.year_of_completion))

    def edit(self, obj):
        prop = Property.objects.all()
        return format_html('<input type="button" onclick="window.open(`/admin/viya1/client/{}/change/`,`_blank`)"'
                           'value="edit" />'
                           , obj.id)
    def profil(self, obj):
        prop = Property.objects.all()
        return format_html('<input type="button" onclick="window.open(`open_profile/{}/change/` )"'  
                           'value="show profil" />'
                           , obj.slug1)

    # { % url
    # 'productsingle'
    # product.slug1 %}

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('open_profile/<slug:slug>/change/', self.open_profile),
        ]
        return my_urls + urls   #<int:post_id>

    def open_profile(self, request, slug ):  #post_id
        clientdata = Client.objects.all()
        slug_1 = Client.objects.get(slug1=slug)
        phone = ClientContact.objects.filter(client_key= slug_1.id)
        reference = References.objects.filter(client_key=slug_1.id)
        client_document = ClientDocuments.objects.filter(client_key= slug_1.id)
        family_document = FamilyDocuments.objects.filter(client_key= slug_1.id)

        # slug_1 = Client.objects.get(slug1=slug)
        # members = FamilyMember.objects.get(client_key=slug_1.id)
        # print(members)

        if request.method == 'POST':
            student = ClientDocumentsForm(request.POST, request.FILES)
            if student.is_valid():
                handle_uploaded_file(request.FILES['client_dokument'])
                model_instance = student.save(commit=False)
                model_instance.save()
                # return HttpResponse("File uploaded successfully")
            student = ClientDocumentsForm()
            context = {
                'slug_1': slug_1,
                # 'posts': posts,
                'phone': phone,
                'reference': reference,
                'client_document': client_document,
                'form': student,
                # 'family_document': family_document
            }

            # print("print context", context)
            return render(request,   'admin/viya1/client/profil.html', context)


        # posts = get_object_or_404(Client, id=post_id)
        # posts = Client.objects.get(pk=pk)
        # if request.method == "POST":
        #      link = 'jjj'
        #     csv_file = request.FILES["csv_file"]
        #     reader = csv.reader(csv_file)
        #
        #     self.message_user(request, "Your csv file has been imported")
        #     return redirect("..")
        # form = ScrapData()
        # data = {"form": form}
        # print("data", data)

        else:
            student = ClientDocumentsForm()
            context = {
                'slug_1': slug_1,
                # 'posts': posts,
                'phone': phone,
                'reference': reference,
                'client_document': client_document,
                'form': student
                # 'family_document': family_document
            }

            # print("print context", context)
            return render(request,   'admin/viya1/client/profil.html', context)


# templates/admin/viya1/client/profil.html
# (`/media/{}`,`_blank`)


admin.site.register(Client, ClientAdmin)

#
# class StudentEnrollmentInline(admin.TabularInline):
#     model = Enrollment
#     readonly_fields=('id',)


# class StudentEnrollmentInline(admin.TabularInline):
#     model = Enrollment
#     readonly_fields=('student_enrollment_id',)
#
#     def student_enrollment_id(self, obj):
#         return obj.id


#
# clientdata = Client.objects.all()
# # slug_1 = Client.objects.get(slug1=slug
# # posts = Client.objects.get(pk=pk)
#
# print (clientdata)