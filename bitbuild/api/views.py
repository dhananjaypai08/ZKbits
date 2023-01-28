from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product
from .serializers import ProductSerializer


# Create your views here.
@api_view(['GET'])
def api(request):
    return Response("URL Patterns")

@api_view(['GET'])
def view(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    
    return Response(serializer.data, 200)

@api_view(['PUT'])
def update(request, id):
    product = Product.objects.get(id=id)
    serializer = ProductSerializer(product, request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response("Item not Updated", 400)

@api_view(['DELETE'])
def delete(request, id):
    product = Product.objects.get(id=id)
    product.delete()
    return Response("Item Deleted", 200)

@api_view(['POST'])
def add(request):
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, 200)
    return Response("Item Not Added", 400)

    
