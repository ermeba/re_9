
from django.db import models
# from clients.models import UserProfileInfo
from django.utils import timezone
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from django.urls import reverse

# choices used in admin
type_choices = ((0, 'Villa'), (1, 'Apartment'), (2, 'Shop'), (3, 'Land'))
status_choice = ((0, 'Sale'), (1, 'Sold'), (2, 'Resale'), (3, 'NoInfo'))
city_choice = ((0, 'Istambul'), (1, 'Antalya'), (2, 'Izmit'), (3, 'Konya'))
false_true_choice = ((0, 'No'), (1, 'Yes'))
district_choice = ((0, 'Uskudar'), (1, 'Umraniye'), (2, 'Fatih'), (3, 'Eminonu'))
sours_choice = ((0, 'Zeray'), (1, 'www.sahibinden.com'), (2, 'www.hepsiemlak.com'), (3, 'https://www.bankadan.com/'))
project_choice = ((1, 'completed'), (2, 'uncompleted'))
type_project_choice = ((1, 'Villa Complex'), (2, 'Apartment Complex'))
partner_choice  = ((1, 'Present partner'), (2, 'Past partner'))
# # Tables for Property
# class City(models.Model):
#     # city_id = models.AutoField(primary_key=True)
#     city = models.IntegerField(choices=city_choice, default=0)
#     next_to_sea = models.IntegerField(choices=false_true_choice, default=0)
#
#
# class District(models.Model):
#     # district_id = models.AutoField(primary_key=True)
#     district = models.IntegerField(choices=district_choice, default=0)
#     next_to_sea = models.IntegerField(choices=false_true_choice, default=0)
#
#
# class Neighborhood(models.Model):
#     # neighborhood_id = models.AutoField(primary_key=True)
#     district = models.IntegerField(choices=district_choice, default=0)
#     next_to_sea = models.IntegerField(choices=false_true_choice, default=0)
#
#
# class Place(models.Model):
#     # city_id = models.AutoField(primary_key=True)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city1')
#     district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district1')
#     neighborhood = models.ForeignKey(Neighborhood, on_delete=models.CASCADE, related_name='neighborhood1')





class City(models.Model):
    name = models.CharField(max_length=100, default=timezone.now())

    def __str__(self):
        return self.name


class Division(models.Model):
    name = models.CharField(max_length=20, default=timezone.now())
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='divisions')

    def __str__(self):
        return self.name


class District(models.Model):
    name=models.CharField(max_length=20, default=timezone.now())
    division = models.ForeignKey(Division, on_delete=models.CASCADE,  related_name='districts')

    def __str__(self):
        return self.name


class SubDistrict(models.Model):
    name = models.CharField(max_length=20, default=timezone.now())
    district = models.ForeignKey(District,on_delete=models.CASCADE, related_name='subdistricts')

    def __str__(self):
        return self.name


class Address(models.Model):
    addressOf = models.CharField(max_length=100, default=timezone.now() )
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='city_set')
    division = models.ForeignKey(Division, on_delete=models.SET_NULL, null=True, blank=True, related_name='division_set')
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True, related_name='district_set')
    subdistrict = models.ForeignKey(SubDistrict, on_delete=models.SET_NULL, null=True, blank=True, related_name='subdistrict_set')

    def __str__(self):
        return self.addressOf


class Property(models.Model):
    offer = models.CharField(max_length=30, default='no title added')
    name = models.CharField(max_length=30, default='no title added')
    created_on = models.DateTimeField(default=timezone.now)
    advert_no = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    advert_created_on = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1000)
    square_meter_brut = models.IntegerField(default=0)
    square_meter_net = models.IntegerField(default=0)
    nr_of_rooms = models.CharField(max_length=3)
    nr_of_bathrooms = models.IntegerField(default=0)
    nr_of_floors = models.IntegerField(default=0)
    position_of_floor = models.IntegerField(default=0)
    furniture = models.BooleanField(default=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city', default=1)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division', default=1)
    address = models.CharField(max_length=300, default='no address')
    status = models.BooleanField(default=True)
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address',  default=1)
    sours = models.IntegerField(choices=sours_choice, default=0)
    photo = models.ImageField(upload_to='property/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdf/', blank=True, null=True)

    def image_preview(self):
        if self.photo:
            return mark_safe('<img src="{0}" width="150" height="120" />'.format(self.photo.url))
        else:
            return '(No image)'

    # def colored_first_name(self):
    #     return format_html(
    #         '<span style="color: #{};">{}</span>',
    #         self.color_code,
    #         self.first_name,
    #     )
    #
    # colored_first_name.admin_order_field = 'title_from_viya'


class PropertySingle(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_p')
    photo = models.ImageField(upload_to='property/foto', blank=True, null=True)


class Type(models.Model):
    # type_id = models.AutoField(primary_key=True)
    type = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property')
    type_of_property = models.IntegerField(choices=type_choices, default=0)


class Status(models.Model):
    # status_id = models.AutoField(primary_key=True)
    status = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property1')
    status_of_property = models.BooleanField(default=True)


class Seller(models.Model):
    seller = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_seller')
    name = models.CharField(max_length=100, default='did not add seller name')
    work_phone_nr = models.CharField(max_length=100, default='no work phone')
    personal_phone_nr = models.CharField(max_length=100, default='no personal phone')
    company_name = models.CharField(max_length=100, default='no company name')
    status_of_property = models.IntegerField(choices=status_choice, default=0)


class Sours(models.Model):
    # status_id = models.AutoField(primary_key=True)
    sours = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_sours')
    sours_of_ads = models.IntegerField(choices=sours_choice, default=0)


class Contact(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=17)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return self.name


# Tables for Partners
class Partner(models.Model):

    status_of_partner = models.IntegerField(choices=partner_choice, default=0)
    name_of_company = models.CharField(max_length=300, default='name of company')
    year_of_establishment = models.CharField(max_length=300, default='year')
    address = models.CharField(max_length=300, default='year')
    phone_number = models.CharField(max_length=300, default='phone number')
    number_of_project = models.IntegerField(default=0)
    description = models.CharField(max_length=500)
    logo = models.ImageField(upload_to='partner/', blank=True, null=True)
    website = models.CharField(max_length=100, default='link')

    def image_preview(self):
        if self.logo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.logo.url))
        else:
            return '(No image)'


# # Tables for Projects
class Project(models.Model):
    project = models.ForeignKey(Partner, on_delete=models.CASCADE, default='No company', related_name='partner_project')
    name_of_project = models.CharField(max_length=300, default='name')
    status_of_project = models.IntegerField(choices=project_choice, default=0)
    year_of_completion = models.CharField(max_length=300, default='year')
    type_of_project = models.IntegerField(choices=type_project_choice, default=0)
    description = models.CharField(max_length=1000, default='description')
    address = models.CharField(max_length=300, default='year')
    phone_number = models.CharField(max_length=300, default='phone number')
    logo = models.ImageField(upload_to='partner/', blank=True, null=True)
    website = models.CharField(max_length=100, default='link')

    def image_preview(self):
        if self.logo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.logo.url))
        else:
            return '(No image)'

#
# class Features(models.Model):
#     feature = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='partner_project')
#     name_of_feature = models.CharField(max_length=300, default='feature name')
#     name_of_feature_Turkish = models.CharField(max_length=300, default='feature name')


# Tables for Clients
class Client(models.Model):
    name = models.CharField(max_length=300, default='name')
    surname = models.CharField(max_length=300, default='surname')
    birthday = models.DateTimeField(default=timezone.now)
    photo = models.ImageField(upload_to='client/', blank=True, null=True)

    def image_preview(self):
        if self.photo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.photo.url))
        else:
            return '(No image)'


class ClientContact(models.Model):
    phone_nr = models.CharField(max_length=300, default='phone number')
    address = models.CharField(max_length=300, default='surname')
    foreign_key = models.ForeignKey(Client, on_delete=models.CASCADE, default='No company', related_name='personID')


class FamilyMember(models.Model):
    member_id = models.IntegerField()
    name = models.CharField(max_length=300, default='name')
    surname = models.CharField(max_length=300, default='surname')
    person_family = models.ForeignKey(Client, on_delete=models.CASCADE, default='no person key', related_name='')


class Relationships(models.Model):
    relationship = models.CharField(max_length=300, blank=False, null=False)
    foreign_key = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, default='No company', related_name='memberId')


class References(models.Model):
    reference_id = models.CharField(max_length=500)
    reference_name = models.CharField(max_length=500, default='no reference')
    foreign_key = models.ForeignKey(Client, on_delete=models.CASCADE, default='no client', related_name='personID' )


class FamilyDocuments(models.Model):
    name_of_document = models.CharField(max_length=300)
    foreign_key = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='memberID')


class ClientDocuments(models.Model):
    name_of_document = models.CharField(max_length=300)
    foreign_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='memberID')








