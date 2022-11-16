from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import *
from django.http import JsonResponse


class DivisionListAPIView(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        city = request.data['city']
        division = {}
        if city:
            divisions = City.objects.get(id=city).divisions.all()
            division = {pp.name:pp.id for pp in divisions}
        return JsonResponse(data=division, safe=False)


class DistrictListAPIView(APIView):
    permission_classes=[IsAuthenticated,]
    def post(self,request,format=None):
        division = request.data['division']
        district = {}
        if division:
            districts = Division.objects.get(id=division).districts.all()
            district = {pp.name:pp.id for pp in districts}
        return JsonResponse(data=district, safe=False)


class SubDistrictListAPIView(APIView):
    permission_classes=[IsAuthenticated,]

    def post(self, request,format=None):
        district=request.data['district']
        subdistrict={}
        if district:
            subdistricts=District.objects.get(id=district).subdistricts.all()
            subdistrict={pp.name:pp.id for pp in subdistricts}
        return JsonResponse(data=subdistrict, safe=False)