from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework import filters
from .models import Banks, Branches
from .serializers import BankSerializer, BranchSerialzier
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import status


class AutoCompleteView(ListAPIView, LimitOffsetPagination):
    """Autocomplete API view for getting possible matches on the basis of branch name """
    serializer_class = BranchSerialzier
    renderer_classes = [JSONRenderer]

    def get_queryset(self):
        branch = self.request.query_params.get('q')
        if branch:
            queryset = Branches.objects.filter(branch__contains=branch).order_by('ifsc')
            return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = BranchSerialzier(queryset, many=True)
        if not queryset:
            return Response({'message': 'Branch not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(data=serializer.data)


class LargeResultsSetPagination(PageNumberPagination):
    """Pagination Controls"""
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000


class SearchView(ListAPIView, LimitOffsetPagination):
    """Search API view for getting the possible matches across all columns and rows"""
    serializer_class = BranchSerialzier
    queryset = Branches.objects.all().order_by('ifsc')
    filter_backends = [filters.SearchFilter]
    search_fields = ['city', 'district', 'state', 'ifsc', 'address', 'bank__name', 'branch']
    renderer_classes = [JSONRenderer]
