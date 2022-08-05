# from django.db import models
#
# # Create your models here.
#
#
# # Tables for Partners
# from django.utils.safestring import mark_safe
#
#
# class Partner(models.Model):
#     partner = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_partners')
#     status_of_property = models.IntegerField(choices=status_choice, default=0)
#     name_of_company = models.CharField(max_length=300, default='name of company')
#     year_of_establishment = models.CharField(max_length=300, default='year')
#     address = models.CharField(max_length=300, default='year')
#     phone_number = models.CharField(max_length=300, default='phone number')
#     number_of_project = models.IntegerField(default=0)
#     description = models.CharField(max_length=500)
#     logo = models.ImageField(upload_to='partner/', blank=True, null=True)
#
#     def image_preview(self):
#         if self.logo:
#             return mark_safe('<img src="{0}" width="130" height="130" />'.format(self.logo.url))
#         else:
#             return '(No image)'
#
#
# # # Tables for Projects
# class Project(models.Model):
#     project = models.ForeignKey(Partner, on_delete=models.CASCADE, related_name='partner_project')
#     name_of_project = models.CharField(max_length=300, default='year')
#     status_of_project = models.IntegerField(choices=project_choice, default=0)
#     type_of_project = models.IntegerField(choices=type_project_choice, default=0)
#     description = models.CharField(max_length=1000, default='description')
#
#
# class Features(models.Model):
#     feature = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='partner_project')
#     name_of_feature = models.CharField(max_length=300, default='feature name')
#     name_of_feature_Turkish = models.CharField(max_length=300, default='feature name')
