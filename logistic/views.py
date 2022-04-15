from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet
import re
from django.db.models import Q
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def get_queryset(self):
        queryset = Stock.objects.all()
        simbol = "^[А-Я а-я a-z A-Z 0123456789]"
        pattern = re.compile(simbol)
        product_name = self.request.query_params.get('products')
        if product_name is not None:
            if product_name.isdigit():
                return Stock.objects.select_related().filter(products=product_name)
            elif pattern.search(product_name):
                queryset = Stock.objects.filter(
                    Q(products__title__startswith=product_name) | Q(products__description__startswith=product_name))
                return queryset
        return queryset

