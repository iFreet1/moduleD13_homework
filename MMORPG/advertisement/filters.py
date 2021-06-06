from django_filters import FilterSet
from .models import Response


class ResponseFilter(FilterSet):
    class Meta:
        model = Response
        fields = {
            'post__header': ['contains'],
            'text': ['contains'],
        }