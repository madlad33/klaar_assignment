from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import filters
from .models import Banks, Branches
from .serializers import BankSerializer, BranchSerialzier
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound,ParseError


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination Controls"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class AutoCompleteView(ListAPIView, LimitOffsetPagination):
    """Autocomplete API view for getting possible matches on the basis of branch name """
    serializer_class = BranchSerialzier
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        branch = self.request.query_params.get('q',None)
        if branch:
            queryset = Branches.objects.filter(branch__contains=branch).order_by('ifsc')
            if queryset:
                return queryset
            else:
                raise NotFound("Branch not found")
        else:
            raise ParseError("Branch name not supplied")


class SearchView(ListAPIView, LimitOffsetPagination):
    """Search API view for getting the possible matches across all columns and rows"""
    serializer_class = BranchSerialzier
    queryset = Branches.objects.all().order_by('ifsc')
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'district', 'state', 'ifsc', 'address', 'bank__name', 'branch']
    renderer_classes = [JSONRenderer]
