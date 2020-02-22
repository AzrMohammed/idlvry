import django_filters
import widget_tweaks
# from simple_forms.apps.core.models import Order
from django_filters import DateFilter

from .models import *

class OrderFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="created_at", lookup_expr='gte')
    # end_date = DateFilter(field_name="created_at", lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['user_customer', 'date_created', 'delivery_charges', 'status_note', 'slug', 'updated_at']
