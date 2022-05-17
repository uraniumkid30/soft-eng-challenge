from rest_framework.views import APIView
from applications.account.selectors import user_list
from applications.api.pagination import CustomPaginator
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from applications.account.serializers import FilterSerializer, OutputSerializer


class UserListApi(APIView):
    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = OutputSerializer

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)
        payload = {
            "request": request,
            "query_set": users,
            "serializer": OutputSerializer,
        }
        paginator_response = CustomPaginator(**payload)
        return paginator_response.data
