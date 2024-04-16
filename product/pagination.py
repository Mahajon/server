from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = 'max'
    max_page_size = 100
    page_query_param = 'page'

    def get_paginated_response(self, data):
        # create a showing string to show the range of items being shown
        start_index = (self.page.number - 1) * self.page_size + 1
        end_index = min(self.page.number * self.page_size, self.page.paginator.count)
        # if end_index > self.page.paginator.count:
        #     end_index = self.page.paginator.count
        # showing = f'{start_index}-{end_index} of {self.page.paginator.count}'
        return Response({
            'links':{
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'pages':{
                'current': self.page.number,
                'total': self.page.paginator.num_pages,
            },
            'items':{
                'start': start_index,
                'end': end_index,
                'total': self.page.paginator.count
            },
            'results': data
        })




class NoPagination(pagination.PageNumberPagination):
    page_size = 1000000
    page_size_query_param = 'page_size'
    max_page_size = 1000000
    page_query_param = 'page'