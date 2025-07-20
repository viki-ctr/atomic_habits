from rest_framework import pagination


class HabitPagination(pagination.PageNumberPagination):
    """Кастомная пагинация для привычек"""
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        response.data.update({
            'total_pages': self.page.paginator.num_pages,
            'current_page': self.page.number,
        })
        return response
