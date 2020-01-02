
from django.urls import path
from base_app import views

app_name = 'base_app'

urlpatterns =[
path('',views.index, name = "index"),
path('home/',views.index, name = "tab1"),
path('register/',views.register, name = "register"),
path('register_customer_care/',views.register_customer_care, name = "register_customer_care"),
path('login/',views.user_login, name = "login"),
path('logout/',views.user_logout, name = "logout"),
path('delivery_agents/',views.delivery_agents, name = "delivery_agents"),
path('customer_care_executive/',views.customer_care_executive, name = "customer_care_executive"),
path('orders_list/',views.orders_list, name = "orders_list"),
path('customer_list/',views.customer_list, name = "customer_list"),
path('order_create/',views.order_create, name = "order_create"),
path('get_da_details/',views.get_da_details, name = "get_da_details"),
path('change_user_status/',views.change_user_status, name = "change_user_status"),
path('change_order_status/',views.change_order_status, name = "change_order_status"),
path('get_order_details/',views.get_order_details, name = "get_order_details"),
path('get_user_order_details/',views.get_user_order_details, name = "get_user_order_details"),




]
