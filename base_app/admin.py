from django.contrib import admin
from base_app.models import UserProfileInfo, Order, OrderItem, ItemMeasuementUnit, Business, DaProfile
# Register your models here.

admin.site.register(UserProfileInfo)
admin.site.register(DaProfile)
admin.site.register(Business)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ItemMeasuementUnit)

# admin.site.register(Webpage)
