from django.shortcuts import render
from .models import car_list, Showroomlist, Review
from .api_file.serializers import carSerializers, ShowroomlistSerializer, ReviewSerializers
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from rest_framework import mixins, generics

class ReviewDetails(mixins.RetrieveModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()  # Replace `YourModel` with your actual model name
    serializer_class = ReviewSerializers

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class Reviewlist(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Review.objects.all()  # Replace `YourModel` with your actual model name
    serializer_class = ReviewSerializers  # Replace `YourSerializer` with your actual serializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)



# Showroom Views
class Showroom_view(APIView):
    # authentication_classes = [BasicAuthentication]
    # # permission_classes = [IsAuthenticated]
    # # permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


    def get(self, request):
        showroom = Showroomlist.objects.all()
        serializer = ShowroomlistSerializer(showroom, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        serializer = ShowroomlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class showroom_details(APIView):
    def get(self, request, pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomlistSerializer(showroom)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
        except Showroomlist.DoesNotExist:
            return Response({'Error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ShowroomlistSerializer(showroom, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            showroom = Showroomlist.objects.get(pk=pk)
            showroom.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Showroomlist.DoesNotExist:
            return Response({'Error': 'Showroom not found'}, status=status.HTTP_404_NOT_FOUND)


# Car Views
@api_view(['GET', 'POST'])
def car_list_view(request):
    if request.method == 'GET':
        car = car_list.objects.all()
        serializer = carSerializers(car, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = carSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def car_detail_view(request, pk):
    try:
        car = car_list.objects.get(pk=pk)
    except car_list.DoesNotExist:
        return Response({'Error': 'Car not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = carSerializers(car)
        return Response(serializer.data)

    if request.method == 'PUT':
        serializer = carSerializers(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'DELETE':
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
