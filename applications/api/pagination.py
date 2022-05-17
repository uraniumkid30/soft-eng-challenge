from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


class CustomPageNumberPagination(PageNumberPagination):
    DEFAULT_PAGE = 1
    page = DEFAULT_PAGE
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total_page", self.page.paginator.num_pages),
                    ("count", self.page.paginator.count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                    (
                        "currentPage",
                        int(
                            self.request.GET.get("page", self.DEFAULT_PAGE)
                        ),  # can not set default = self.page
                    ),
                ]
            )
        )

    def get_paginated_response_revised(self, data):
        return Response(
            {
                "links": {
                    "next": self.get_next_link(),
                    "previous": self.get_previous_link(),
                },
                "itemsCount": self.page.paginator.count,
                "currentPage": int(
                    self.request.GET.get("page", self.DEFAULT_PAGE)
                ),  # can not set default = self.page
                "page_size": int(
                    self.request.GET.get(self.page_size_query_param, self.page_size)
                ),
                "totalPages": self.page.paginator.num_pages,
                "results": data,
            }
        )


class CustomPaginator:
    def __init__(self, **kwargs):
        request = kwargs.get("request")
        pagination_type = kwargs.get("pagination_type", "PNP")
        query_set = kwargs.get("query_set")
        serializer = kwargs.get("serializer")
        if pagination_type == "PNP":
            max_page_size = kwargs.get("max_page_size", 50)
            page_size = kwargs.get("page_size", 1)
            paginator = CustomPageNumberPagination()
            context = paginator.paginate_queryset(query_set, request)
            ser = serializer(context, many=True)
            self.data = paginator.get_paginated_response(ser.data)
        else:
            # paginator is LOP
            max_page_size = kwargs.get("max_page_size", 50)
            page_size = kwargs.get("page_size", 20)
            lim_paginator = LimitOffsetPagination()
            lim_paginator.max_limit = max_page_size
            lim_paginator.default_limit = page_size
            lim_context = lim_paginator.paginate_queryset(query_set, request)
            lim_serializer = serializer(lim_context, many=True)
            self.data = lim_paginator.get_paginated_response(lim_serializer.data)
