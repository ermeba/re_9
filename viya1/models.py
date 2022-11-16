
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
sours_choice = ((0, 'Unknown'), (1, 'www.sahibinden.com'), (2, 'www.hepsiemlak.com'), (3, 'www.bankadan.com'),
               (4, 'Partner'))
project_choice = ((1, 'completed'), (2, 'uncompleted'))


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
    name=models.CharField(max_length=40, default=timezone.now())
    division = models.ForeignKey(Division, on_delete=models.CASCADE,  related_name='districts')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='District_City', null=True, blank=True,)

    def __str__(self):
        return self.name


class SubDistrict(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    district = models.ForeignKey(District,on_delete=models.CASCADE, related_name='subdistricts', null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE,  related_name='SubDistrict_Division', null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='SubDistrict_City', null=True, blank=True)
    post_code = models.CharField(max_length=5, null=True, blank=True)

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
    advert_no = models.CharField(max_length=300, blank=True, null=True)
    price = models.IntegerField(null=True, blank=True)
    advert_created_on = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=1000, null=True, blank=True)
    square_meter_brut = models.IntegerField(default=0)
    square_meter_net = models.IntegerField(default=0)
    nr_of_rooms = models.CharField(max_length=10)
    nr_of_bathrooms = models.IntegerField(default=0)
    nr_of_floors = models.IntegerField(default=0)
    position_of_floor = models.IntegerField(default=0)
    furniture = models.BooleanField(default=True)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city', default=1)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division', default=1)
    address = models.CharField(max_length=300, default='no address')
    status = models.BooleanField(default=True, null=True, blank=True)
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address',  default=1)
    sours = models.IntegerField(choices=sours_choice, default=0)
    photo = models.ImageField(upload_to='property/', blank=True, null=True)
    pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
    link = models.URLField(max_length=500, blank=True, null=True)


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

# class Property1(models.Model):
#     offer = models.CharField(max_length=30, default='no title added')
#     name = models.CharField(max_length=30, default='no title added')
#     created_on = models.DateTimeField(default=timezone.now)
#     advert_no = models.CharField(max_length=300, blank=True, null=True)
#     price = models.IntegerField(default=0)
#     advert_created_on = models.DateTimeField(default=timezone.now)
#     description = models.CharField(max_length=1000)
#     square_meter_brut = models.IntegerField(default=0)
#     square_meter_net = models.IntegerField(default=0)
#     nr_of_rooms = models.CharField(max_length=3)
#     nr_of_bathrooms = models.IntegerField(default=0)
#     nr_of_floors = models.IntegerField(default=0)
#     position_of_floor = models.IntegerField(default=0)
#     furniture = models.BooleanField(default=True)
#     latitude = models.FloatField(default=0.0)
#     longitude = models.FloatField(default=0.0)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city1', default=1)
#     division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division1', default=1)
#     address = models.CharField(max_length=300, default='no address')
#     status = models.BooleanField(default=True)
#     # address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='address',  default=1)
#     sours = models.IntegerField(choices=sours_choice, default=0)
#     photo = models.ImageField(upload_to='property/', blank=True, null=True)
#     pdf = models.FileField(upload_to='pdf/', blank=True, null=True)
#     link = models.URLField(max_length=500, blank=True, null=True)
#
#     def image_preview(self):
#         if self.photo:
#             return mark_safe('<img src="{0}" width="150" height="120" />'.format(self.photo.url))
#         else:
#             return '(No image)'
#
# class TypeOfEstate1(models.Model):
#     type_name = models.CharField(max_length=300)
#     foreign_key = models.ForeignKey(Property1, on_delete=models.CASCADE, related_name='estate_type_property1')


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

# Table of offers from Partners
type_project_choice = ((1, 'Villa Complex'), (2, 'Apartment Complex'))
partner_choice  = ((1, 'Present partner'), (2, 'Past partner'))


class Partner(models.Model):
    status_of_partner = models.IntegerField(choices= partner_choice, default=0)
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


class Features(models.Model):
    feature = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='partner_project')
    name_of_feature = models.CharField(max_length=300, default='feature name')
    name_of_feature_Turkish = models.CharField(max_length=300, default='feature name')

###################################################################################################################
############## New data base for partners#######################################################################
# # Tables for Projects

class PhoneNumber(models.Model):
    person_name = models.CharField(max_length=300, blank=True, null=True )
    person_surname = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)


class Emails(models.Model):
    person_name = models.CharField(max_length=300, blank=True, null=True )
    person_surname = models.CharField(max_length=300, blank=True, null=True)
    phone_number = models.CharField(max_length=300, blank=True, null=True)


class OfferAddress(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_offeraddress', null=True, blank=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='division_offeraddress', null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='district_offeraddress', null=True, blank=True)
    subdistrict = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, related_name='district_offer', null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)


class OfferContact(models.Model):
    address = models.ForeignKey(OfferAddress, on_delete=models.CASCADE, related_name='address_offer', null=False, blank=False)
    phone = models.ForeignKey(PhoneNumber, on_delete=models.CASCADE, blank=True, null=True)
    email = models.ForeignKey(Emails, on_delete=models.CASCADE, blank=True, null=True)


class OfferProjectPhotos(models.Model):
    photo_project = models.ImageField(upload_to='offers/', blank=True, null=True)


    def image_preview(self):
        if self.photo_project:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.photo_project.url))
        else:
            return '(No image)'


class OfferProjectPlanPhotos(models.Model):
    photo_plan_project = models.ImageField(upload_to='offers/', blank=True, null=True)


    def image_preview(self):
        if self.photo_plan_project:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.photo_plan_project.url))
        else:
            return '(No image)'
class OfferCompany(models.Model):
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
    def __str__(self):
        return self.name_of_company

class OfferProject(models.Model):
    name_of_project = models.CharField(max_length=300, null=False, blank=False)
    status_of_project = models.IntegerField(choices=project_choice,null=True, blank=True)
    year_of_completion = models.CharField(max_length=300, null=False, blank=False)
    type_of_project = models.IntegerField(choices=type_project_choice, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    address = models.CharField(max_length=300, null=True, blank=True)
    logo = models.ImageField(upload_to='partner/', blank=True, null=True)
    website = models.CharField(max_length=100, default='link')
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, related_name='contact_offerproject',null=True, blank =True)
    company = models.ForeignKey(OfferCompany, on_delete=models.CASCADE, related_name='offercompany',null=True, blank =True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='OfferProject_City', blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='OfferProject_Division', blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='OfferProject_District', blank=True, null=True)
    offers = models.ForeignKey(OfferProjectPhotos, on_delete=models.CASCADE, related_name='OfferProject_OfferProjectPhotos', blank=True, null=True)
    offers_project = models.ForeignKey(OfferProjectPlanPhotos, on_delete=models.CASCADE, related_name='OfferProject_OfferProjectPlanPhotos', blank=True, null=True)

    def image_preview(self):
        if self.logo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.logo.url))
        else:
            return '(No image)'

    def __str__(self):
        return self.name_of_project



class OfferType(models.Model):
    type_name = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.type_name


class OfferFeatures(models.Model):
    name_of_feature = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return self.name_of_feature

class OfferRoomTypeExpression(models.Model):
    name = models.CharField(max_length=300, null=True, blank=True)
    def __str__(self):
        return self.name



class Offers(models.Model):
    offer_name = models.CharField(max_length=300, null=False, blank=False)
    offer_type = models.ForeignKey(OfferType, on_delete=models.CASCADE, related_name='offer_type', blank=True, null=True )
    project = models.ForeignKey(OfferProject, on_delete=models.CASCADE, related_name='Offers_OfferProject', blank=True,null=True)
    company = models.ForeignKey(OfferCompany, on_delete=models.CASCADE, related_name='Offers_OfferCompany', blank=True, null=True)
    # room_type = models.ForeignKey(OfferRoomTypeExpression, on_delete=models.CASCADE, related_name='Offers_OfferRoomTypeExpression', null=True, blank=True)
    contact = models.ForeignKey(OfferContact, on_delete = models.CASCADE, related_name= 'Offers_OfferContact', blank=True, null=True)
    features = models.ForeignKey(OfferFeatures, on_delete=models.CASCADE, related_name='Offers_OfferFeatures', blank=True, null=True)
    address = models.ForeignKey(OfferAddress, on_delete=models.CASCADE, related_name='Offers_OfferAddress', blank=True, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_offer', blank=True, null=True)
    division = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='Offers_Division', blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='Offers_District', blank=True, null=True)
    # subdistrict = models.ForeignKey(SubDistrict, on_delete=models.CASCADE, related_name='Offers_SubDistrict', blank=True, null=True)
    photo = models.ImageField(upload_to='offers/', blank=True, null=True)

    def image_preview(self):
        if self.photo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.photo.url))
        else:
            return '(No image)'

class OfferPhotos(models.Model):
    photo = models.ImageField(upload_to='offers/', blank=True, null=True)
    offers = models.ForeignKey(Offers, on_delete=models.CASCADE, related_name = 'offerphotos_offers', blank=True, null=True)

    def image_preview(self):
        if self.photo:
            return mark_safe('<img src="{0}" width="80" height="60" />'.format(self.photo.url))
        else:
            return '(No image)'


class OfferDescription(models.Model):
    short_description = models.CharField(max_length=500, blank=True, null=True )
    extended_description = models.CharField(max_length=1000, blank=True, null=True)
    description = models.ForeignKey(Offers, on_delete= models.CASCADE, related_name='description_offer', blank=True, null=True)

class OfferPrice(models.Model):
    min_price = models.IntegerField(null=False, blank=False)
    max_price = models.IntegerField(null=False, blank=False)
    price = models.ForeignKey(Offers, on_delete= models.CASCADE, related_name= 'price_offer', blank=True, null=True)


class OfferSqm(models.Model):
    min_sqm = models.IntegerField(null=True, blank=True)
    max_sqm = models.IntegerField(null=True, blank=True)
    garden_meters = models.IntegerField(null=True, blank=True)
    total_meters = models.IntegerField(null=True, blank=True)
    sqm = models.ForeignKey(Offers, on_delete= models.CASCADE, related_name = 'sqm_offer', blank=True, null=True)

# Tables for Partners
from django.template.defaultfilters import slugify
nr_of_rooms_choices = ((0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, '8'), (8, '9'), (9, '10'),
                (10, '11'), (11, '12'),(12, '13'), (13, '14'), (14, '15'), (15, '16'), (16, '17'), (17, '18'),
                (18, '19'), (19, '20'), (20, '21') )

nr_of_bedrooms_choices = ((0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, '8'), (8, '9'), (9, '10'),
                (10, '11'), (11, '12'),(12, '13'), (13, '14'), (14, '15'), (15, '16'), (16, '17'), (17, '18'),
                (18, '19'), (19, '20'), (20, '21') )

nr_of_bathrooms_choices = ((0, '1'), (1, '2'), (2, '3'), (3, '4'), (4, '5'), (5, '6'), (6, '7'), (7, '8'), (8, '9'), (9, '10'),
                (10, '11'), (11, '12'),(12, '13'), (13, '14'), (14, '15') )

# class OfferRoomType(Offers):
#     nr_of_rooms = models.IntegerField(choices=nr_of_rooms_choices, null=True, blank=True)
#     nr_of_bedrooms = models.IntegerField(choices=nr_of_bedrooms_choices,null=True, blank=True)
#     nr_of_bathrooms = models.IntegerField(choices=nr_of_bedrooms_choices,null=True, blank=True)
#     room_type = models.ForeignKey(OfferRoomTypeExpression, on_delete=models.CASCADE, related_name='room_tupe_offerroomtype', null=True, blank=True)
#     offer = models.ForeignKey(Offers, on_delete= models.CASCADE, related_name = 'OfferRoomType_Offers', blank=True, null=True)
#     room_type1 = models.CharField(max_length=10, blank=True, null=True)


    # def save(self):
    #     self.room_type = str(self.nr_of_rooms)+ " + "+str(self.nr_of_bedrooms)
    #     return super(OfferRoomType, self).save()
    #
    # def __str__(self):
    #     return str(self.nr_of_rooms)+ " + "+str(self.nr_of_bedrooms)


######################################################################################################################


status_choice_client = ((0, 'Starting'), (1, 'Processing'), (2, 'Finished'), (3,  'Canceled'))

# Tables for Clients
class Client(models.Model):
    name = models.CharField(max_length=300, default='no name')
    surname = models.CharField(max_length=300, default='no surname')
    nationality = models.CharField(max_length=300, blank=True, null=True)
    birthday = models.DateTimeField(default=timezone.now)
    date_of_application = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, default='no address added')
    status = models.IntegerField(choices=status_choice_client, blank=True, null=True)
    photo = models.ImageField(upload_to='client/', blank=True, null=True)
    slug1 = models.SlugField(unique=True, null=True, blank=True)

    def image_preview(self):
        if self.photo:
            return mark_safe('<img src="{0}" width="90" height="90" />'.format(self.photo.url))
        else:
            return '(No image)'
    #
    # def save(self, *args, **kwargs):
    #     if not self.id:
    #         # Newly created object, so set slug
    #         self.slug1 = slugify(self.address)
    #
    # #     super(Client, self).save(*args, **kwargs)
    #
    # def save(self, *args, **kwargs):
    #     self.slug1 = slugify(self.address)
    #     return super(Client, self).save(*args, **kwargs)


contact_choice = ((0, 'Personal'), (1, 'Company'), (2,  'Family'))

class ClientContact(models.Model):
    name_surname = models.CharField(max_length=300, default='name')
    phone_nr = models.CharField(max_length=300, default='phone number')
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients_phone')
    type = models.IntegerField(choices=contact_choice, blank=True, null=True)

# class Relationships(models.Model):
#     relationship_name = models.CharField(max_length=300, blank=False, null=False)


member_choice = ((0, 'Husband'), (1, 'Wife'), (2,  'Child'))


class FamilyMember(models.Model):
    # member_id = models.IntegerField()
    name = models.CharField(max_length=300, default='name')
    surname = models.CharField(max_length=300, default='surname')
    type_relationships = models.IntegerField(choices=member_choice, blank=True, null=True)
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients_members')
    # relationship_key = models.ForeignKey(Relationships, on_delete=models.CASCADE, related_name='member_relationship')


type_choice = ((0, 'Other'), (1, 'Partner'), (2,  'Person'), (3, 'Hotel'))

class References(models.Model):
    # reference_id = models.CharField(max_length=500)
    reference_name = models.CharField(max_length=500, default='no reference')
    type_reference = models.IntegerField(choices=type_choice, default=0)
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_references')

class ReferencesContact(models.Model):
    type = models.IntegerField(choices=type_choice, default=0)
    reference_description = models.CharField(max_length=500, default='no reference', )
    reference_link = models.URLField(max_length=500, blank=True, null=True)
    reference_phone_nr = models.CharField(max_length=500, default='no phone number added')
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='client_references_contact' )


class FamilyDocuments(models.Model):
    name_of_document = models.CharField(max_length=300, default='name of document')
    date_of_upload = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=500, default='description of document')
    family_dokument = models.FileField(upload_to='client/documents/', blank=True, null=True)
    family_member_key = models.ForeignKey(FamilyMember, on_delete=models.CASCADE, related_name='document_member',
                                          blank=True, null=True)
    # relationship_key = models.ForeignKey(Relationships, on_delete=models.CASCADE, related_name='document_relationship')
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='document_client' )


class ClientDocuments(models.Model):
    name_of_document = models.CharField(max_length=300, default='name of document')
    description = models.CharField(max_length=500, default='description of document')
    date_of_upload = models.DateTimeField(default=timezone.now)
    client_dokument = models.FileField(upload_to='client/documents/', blank=True, null=True)
    client_key = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='clients_documents')



