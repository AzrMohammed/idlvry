from django.shortcuts import render
from django.contrib.auth import authenticate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from base_app.forms import UserProfileInfoForm, UserForm, UserFormDa, OrderForm, UserParentForm, UserProfileInfoFormDa, OrderItemForm, DaProfileForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify
import datetime
from base_app.utils import random_string_generator
import string
from base_app import constants, dbconstants
# from django.db import models
from base_app.models import UserProfileInfo, Order, OrderItem, ItemMeasuementUnit, DaProfile
from django.core import serializers
# Create your views here.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from base_app import smsbase
import re
# from itertools import izip


def change_user_status(request):

    print("came changestat")
    username = request.POST['username']
    user_status = request.POST['user_status']

    user_obj = User.objects.get(username=username)
    user_profile = UserProfileInfo.objects.get(user=user_obj)

    # user_profile = UserProfileInfo.objects.get(username=username)

    if user_status == "AT":
        print("useractive")
        user_status = dbconstants.USER_STATUS_DISABLED
    else:
        user_status = dbconstants.USER_STATUS_ACTIVE
        print("userinactive")
    user_profile.user_status = user_status
    user_profile.save()

    return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Status updated"}),
    content_type="application/json")





def customer_list(request):

    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_CONSUMER).order_by('-created_at')
    # user_list = User.objects.all().select_related('user_profile_info')

    # user_profile_list.

    user_list_final = []




    for user_temp in user_list:
        # print("caddd")
        user_meta_raw = User.objects.get(username=user_temp.user)
        # print(user_meta_raw.username)
        user_meta = {}
        user_meta['username'] = user_meta_raw.username
        #
        #
        # user_temp['profile_pic_absolute'] =  appendServerPath(user_temp['profile_pic'])
        # user_temp.profile_pic("aa","aa")
        # pic = user_temp.profile_pic
        # print(pic)
        user_parent_set = {}
        # user_parent_set['profile_pic'] = appendServerPath(user_temp.profile_pic)
        user_parent_set['user_meta'] = user_meta
        user_parent_set['user_profile'] = user_temp
        #
        user_list_final.append(user_parent_set)

    serialized_obj = serializers.serialize('json', user_list)

    print("sizeb:"+ str(user_list.count()))


    page = request.GET.get('page', 1)

    paginator = Paginator(user_list_final, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'base_app/customers.html',  {'state_list':dbconstants.STATE_LIST_DICT, 'users': users})


def index(request):

    print("klsklkl")

    # smsbase.sendOrderCreationMessage()

    order_count = Order.objects.all().count()
    order_delivered_count = 0
    delivery_boy_count = UserProfileInfo.objects.filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT).count()

    customers_count  = UserProfileInfo.objects.filter(user_type = dbconstants.USER_TYPE_CONSUMER).count()

    # delivery_boy_count = 0

    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT)
    # user_list = User.objects.all().select_related('user_profile_info')

    # user_profile_list.

    user_list_final = []
# aas



    for user_temp in user_list:
        # print("caddd")
        user_meta_raw = User.objects.get(username=user_temp.user)
        # print(user_meta_raw.username)
        user_meta = {}
        user_meta['username'] = user_meta_raw.username
        #
        #
        # user_temp['profile_pic_absolute'] =  appendServerPath(user_temp['profile_pic'])
        # user_temp.profile_pic("aa","aa")
        pic = user_temp.profile_pic
        print(pic)
        user_parent_set = {}
        user_parent_set['profile_pic'] = appendServerPath(user_temp.profile_pic)
        user_parent_set['user_meta'] = user_meta
        user_parent_set['user_profile'] = user_temp
        #
        user_list_final.append(user_parent_set)
        # serialized_obja = serializers.serialize('json', [user_parent_set])
        # # # filter(user__username ='azr')
        # # # user_list = User.objects.filter(username ='azr')
        # dataa = {"aSomeModel_json": serialized_obj}
        # ("atitaa")
        # print(dataa)
        #
        #

    serialized_obj = serializers.serialize('json', user_list)



    # profile_check = UserProfileInfo.objects.filter(phone_primary=post_data["phone_primary"], user_type = dbconstants.USER_TYPE_CONSUMER)

    # Order.objects.prefetch_related('user_customer').prefetch_related('user_delivery_agent').all().order_by('-updated_at')




    page = request.GET.get('page', 1)

    paginator = Paginator(user_list_final, 100)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)


    today = datetime.date.today()

    base_dict = {"order_count":order_count, "delivery_boy_count":delivery_boy_count, "order_delivered":order_delivered_count, "customers_count":customers_count, "delivery_agents":users, 'pic_server_prefix':'http://http://167.71.126.94:8000/media/' }
    return render(request, 'base_app/index.html', context = base_dict)

@login_required
def delivery_agents(request):
    # user_profile_list = UserProfileInfo.objects.filter(user_type =dbconstants.DELIVERY_AGENT)
    # user_list = User.objects.filter(user_profile_info__user_type = dbconstants.DELIVERY_AGENT)
    # user_list = UserProfileInfo.objects.all().select_related('user')
    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT).order_by('-updated_at')
    # user_list = User.objects.all().select_related('user_profile_info')

    # user_profile_list.

    user_list_final = []




    for user_temp in user_list:
        # print("caddd")
        user_meta_raw = User.objects.get(username=user_temp.user)
        # print(user_meta_raw.username)
        user_meta = {}
        user_meta['username'] = user_meta_raw.username
        #
        #
        # user_temp['profile_pic_absolute'] =  appendServerPath(user_temp['profile_pic'])
        # user_temp.profile_pic("aa","aa")
        pic = user_temp.profile_pic
        # print(pic)
        user_parent_set = {}
        user_parent_set['profile_pic'] = appendServerPath(user_temp.profile_pic)
        user_parent_set['user_meta'] = user_meta
        user_parent_set['user_profile'] = user_temp
        #
        user_list_final.append(user_parent_set)
        # serialized_obja = serializers.serialize('json', [user_parent_set])
        # # # filter(user__username ='azr')
        # # # user_list = User.objects.filter(username ='azr')
        # dataa = {"aSomeModel_json": serialized_obj}
        # ("atitaa")
        # print(dataa)
        #
        #

    serialized_obj = serializers.serialize('json', user_list)
    # filter(user__username ='azr')
    # user_list = User.objects.filter(username ='azr')
    # dataa = {"SomeModel_json": serialized_obj}
    # print("titaa")
    # print(dataa)
    # print("sizea:"+ str(user_profile_list.count()))
    print("sizeb:"+ str(user_list.count()))


    page = request.GET.get('page', 1)

    paginator = Paginator(user_list_final, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'base_app/delivery_agents.html',  {'state_list':dbconstants.STATE_LIST_DICT, 'users': users, 'pic_server_prefix':'http://167.71.126.94:8000/media/' })


@login_required
def customer_care_executive(request):
    # user_profile_list = UserProfileInfo.objects.filter(user_type =dbconstants.DELIVERY_AGENT)
    # user_list = User.objects.filter(user_profile_info__user_type = dbconstants.DELIVERY_AGENT)
    # user_list = UserProfileInfo.objects.all().select_related('user')
    user_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_CUSTOMER_CARE_EXECUTIVE).order_by('-updated_at')
    # user_list = User.objects.all().select_related('user_profile_info')

    # user_profile_list.

    print(len(user_list))

    user_list_final = []




    for user_temp in user_list:
        # print("caddd")
        user_meta_raw = User.objects.get(username=user_temp.user)
        # print(user_meta_raw.username)
        user_meta = {}
        user_meta['username'] = user_meta_raw.username
        #
        #
        # user_temp['profile_pic_absolute'] =  appendServerPath(user_temp['profile_pic'])
        # user_temp.profile_pic("aa","aa")
        pic = user_temp.profile_pic
        # print(pic)
        user_parent_set = {}
        user_parent_set['profile_pic'] = appendServerPath(user_temp.profile_pic)
        user_parent_set['user_meta'] = user_meta
        user_parent_set['user_profile'] = user_temp
        #
        user_list_final.append(user_parent_set)
        # serialized_obja = serializers.serialize('json', [user_parent_set])
        # # # filter(user__username ='azr')
        # # # user_list = User.objects.filter(username ='azr')
        # dataa = {"aSomeModel_json": serialized_obj}
        # ("atitaa")
        # print(dataa)
        #
        #

    serialized_obj = serializers.serialize('json', user_list)
    # filter(user__username ='azr')
    # user_list = User.objects.filter(username ='azr')
    # dataa = {"SomeModel_json": serialized_obj}
    # print("titaa")
    # print(dataa)
    # print("sizea:"+ str(user_profile_list.count()))
    print("sizeb:"+ str(user_list.count()))


    page = request.GET.get('page', 1)

    paginator = Paginator(user_list_final, 9)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request, 'base_app/customer_care_executive.html',  {'state_list':dbconstants.STATE_LIST_DICT, 'users': users, 'pic_server_prefix':'http://167.71.126.94:8000/media/' })

@login_required
def orders_list(request):

    order_list = Order.objects.prefetch_related('user_customer').prefetch_related('user_delivery_agent').all().order_by('-updated_at')

    order_list_final = []

    for order_temp in order_list:
        # print("caddd")
        # print("cadddw"+str(order_temp.user_customer))
        user_customer_m =User.objects.get(username = order_temp.user_customer)
        user_customer = UserProfileInfo.objects.get(user = user_customer_m)

        user_delivery_agent_m =User.objects.get(username = order_temp.user_delivery_agent)
        user_delivery_agent = UserProfileInfo.objects.get(user=user_delivery_agent_m)

        user_customer.user_location_display = user_customer.location_area +','+user_customer.location_sublocality+","+user_customer.location_city+","+user_customer.location_pincode


        # getting order item

        order_items = OrderItem.objects.filter(order = order_temp)
        print("sizeaaa:"+ str(order_items.count()))

        item_name =""

        for order_item in order_items:
            if item_name != '':
                item_name += ", "+order_item.item_name
            else:
                item_name += order_item.item_name

        order_temp.order_items = item_name

        # getting status text
        order_temp.status = dbconstants.ORDER_STATUS_DIC[order_temp.status]



        # print(user_meta_raw.username)
        order_foreign = {}
        order_foreign['user_customer'] = user_customer
        order_foreign['user_delivery_agent'] = user_delivery_agent

        #
        #
        order_parent_set = {}
        order_parent_set['order_meta'] = order_temp
        order_parent_set['order_foreign'] = order_foreign
        #
        order_list_final.append(order_parent_set)
        # print("sizeb:"+ JsonResponse(json.loads(order_list_final)))
        # serialized_obja = serializers.serialize('json', order_parent_set)
        # # # filter(user__username ='azr')
        # # # user_list = User.objects.filter(username ='azr')
        # dataa = {"aSomeModel_json": serialized_obja}
        # ("atitaa")
        # print(dataa)
        #
        #




    # fetching prerequistis data for screen

    state_list  = dbconstants.STATE_LIST_DICT
    measurements_list = ItemMeasuementUnit.objects.all()
    delivery_agents_list = UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT)

    # for meas in measurements_list:
    #     print("came print m"+meas.name)
    #

    page = request.GET.get('page', 1)

    paginator = Paginator(order_list_final, 9)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    return render(request, 'base_app/orders_list.html',  { 'orders': orders, 'delivery_agents_list':delivery_agents_list, 'measurements_list':measurements_list, 'state_list':state_list })



@login_required
def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('base_app:index'))

def appendServerPath(relative_path):
    a = str(relative_path)
    return constants.SERVER_PREFIX+a


def user_login(request):
    # return HttpResponse("Hi came view")

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        print(username+"+==="+password)

        user = authenticate(request, username = username, password = password)

        if user:
            if user.is_active:
                print('active')
                auth_login(request,user)
                return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Login successful"}),
                content_type="application/json")


                # return HttpResponseRedirect(reverse('base_app:index'))
            else:
                errors_dict = {"DATA":"Not a valid data"}
                return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"2INVALID DATA", "ERRORS": errors_dict}),
                content_type="application/json")

        else:
            errors_dict = {"DATA":"Not a valid data"}
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS": errors_dict}),
            content_type="application/json")

    else:
        print('jdkada')
        return render(request, 'base_app/login.html', {})

def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = random_string_generator(size=8)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = random_string_generator(size=8)
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug

def unique_order_id_generator(instance, new_order_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_order_id is not None:
        order_id = new_order_id
    else:
        order_id = constants.REF_ID_PREF_ORDER+random_string_generator(size=5)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        new_order_id = constants.REF_ID_PREF_ORDER+random_string_generator(size=5)
        # "{ref_id}-{randstr}".format(
        #             ref_id=ref_id,
        #             randstr=random_string_generator(size=8, chars=string.ascii_uppercase)
        #         )
        return unique_order_id_generator(instance, new_order_id=new_order_id)
    return order_id

def unique_order_item_id_generator(instance, new_order_item_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_order_item_id is not None:
        order_item_id = new_order_item_id
    else:
        order_item_id = constants.REF_ID_PREF_ORDER_ITEM+random_string_generator(size=5)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(order_item_id=order_item_id).exists()
    if qs_exists:
        new_order_item_id = constants.REF_ID_PREF_ORDER_ITEM+random_string_generator(size=5)
        return unique_order_item_id_generator(instance, new_order_item_id=new_order_item_id)
    return order_item_id

def unique_ref_id_generator(instance, new_ref_id=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_ref_id is not None:
        ref_id = new_ref_id
    else:
        ref_id = constants.REF_ID_PREF_DELIVERY_AGENT+random_string_generator(size=5)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(ref_id=ref_id).exists()
    if qs_exists:
        new_ref_id = constants.REF_ID_PREF_DELIVERY_AGENT+random_string_generator(size=5)
        # "{ref_id}-{randstr}".format(
        #             ref_id=ref_id,
        #             randstr=random_string_generator(size=8, chars=string.ascii_uppercase)
        #         )
        return unique_ref_id_generator(instance, new_ref_id=new_ref_id)
    return ref_id

def Merge(dict1, dict2):
    (dict2.update(dict1))
    return dict2

#
# def getOrderItemComponemt(request):
#







#
# def grouped(iterable, n):
#     return izip(*[iter(iterable)]*n)


def get_order_details(request):

    if request.method == "POST":
        print("came rewwww")
        # print(request.POST)
        # order_list_final = []
        # order_temp_qset = Order.objects.filter(order_id=request.POST["order_id"]).only('order_id','status', 'user_customer', 'user_delivery_agent')

        # order_temp = Order.objects.only('order_id','status', 'user_customer', 'user_delivery_agent').filter(order_id=request.POST["order_id"])
        # .get(order_id=request.POST["order_id"])
        # print("cameaa")


        # get order details

        # print("ordeR_id"+request.POST["order_id"])

        order_obj = Order.objects.get(order_id=request.POST["order_id"])
        qset_orders = Order.objects.filter(order_id=request.POST["order_id"]).values('order_id', 'status', 'user_customer', 'user_delivery_agent')

        orders_dict = queryset_to_dict(qset_orders)[0]


        print("customer:"+str(order_obj.user_customer))

        # get customer details
        qset_user_customer =User.objects.filter(username = order_obj.user_customer).values('username')
        user_customer_dict = queryset_to_dict(qset_user_customer)[0]

        qset_user_customer_profile = UserProfileInfo.objects.filter(user = User.objects.get(username = order_obj.user_customer)).values('location_pincode','phone_primary','location_area','location_sublocality','location_locality','location_city','location_state','location_pincode')
        user_customer_profile_dict = queryset_to_dict(qset_user_customer_profile)

        customer_details = {}

        customer_details['meta'] = user_customer_dict
        customer_details['profile'] = user_customer_profile_dict

        # get delivery agent details

        qset_user_delivery_agent =User.objects.filter(username = order_obj.user_delivery_agent).values('username')
        user_delivery_agent_dict = queryset_to_dict(qset_user_delivery_agent)[0]



        qset_user_delivery_agent_profile = UserProfileInfo.objects.filter(user = User.objects.get(username = order_obj.user_delivery_agent)).values('location_pincode')
        user_delivery_agent_profile_dict = queryset_to_dict(qset_user_delivery_agent_profile)

        delivery_agent_details = {}

        delivery_agent_details['meta'] = user_delivery_agent_dict
        delivery_agent_details['profile'] = user_delivery_agent_profile_dict


        # user_customer.user_location_display = user_customer.location_area +','+user_customer.location_sublocality+","+user_customer.location_city+","+user_customer.location_pincode
        #
        #
        # # getting order item


        order_items = OrderItem.objects.filter(order = order_obj)
        qset_items = OrderItem.objects.filter(order = order_obj).values('item_name', 'item_quantity', 'measurement_unit')
        user_order_item_dict = queryset_to_dict(qset_items)

        print("sizeaaa:item "+ str( user_order_item_dict))


        item_name =""

        for order_item in order_items:
            if item_name != '':
                item_name += ", "+order_item.item_name
            else:
                item_name += order_item.item_name

        print(item_name)
        order_obj.order_items = item_name

        # getting status text
        order_obj.status = dbconstants.ORDER_STATUS_DIC[order_obj.status]


        # .only('e_name','e_date')

        order_foreign = {}
        # order_foreign['user_customer'] = serializers.serialize('json', [user_customer])
        # order_foreign['user_delivery_agent'] = serializers.serialize('json', [user_delivery_agent])

        # print(order_foreign)
        #
        #
        # order_parent_set = {}
        # order_parent_set['order_meta'] = order_temp
        # order_parent_set['order_foreign'] =  order_foreign
        #
        # order_list_final.append(order_parent_set)

        # user_obj = User.objects.get(username=request.POST["username"])
        # user_profile = UserProfileInfo.objects.get(user=user_obj)
        # da_profile = DaProfile.objects.get(user=user_profile)
        # user_obj_s = serializers.serialize('json', [user_obj])
        # user_profile_s = serializers.serialize('json', [user_profile])

        # user_list_final = []
        # user_list_final.append(order_parent_set)
        # order_details_l = serializers.serialize('json', order_parent_set)
        #

        # user_customer_s = serializers.serialize('json', [user_customer])
        # user_delivery_agent_s = serializers.serialize('json', [user_delivery_agent])
        # order_meta_s = serializers.serialize('json', [order_temp])

        # list_result = [entry for entry in queryset]

        # print(orders_dict['order_id'])
        # for order_id in list_result:
            # print("==="+order_id)

        # return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"DATA FETCHED", "user_customer":user_customer_s, "user_delivery_agent":user_delivery_agent_s, "order_meta":list(order_temp) }),
        return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"DATA FETCHED",  "order_meta":orders_dict, "order_item": user_order_item_dict, 'user_customer':customer_details, 'user_delivery_agent':delivery_agent_details }, indent=4, sort_keys=True, default=str),

            content_type="application/json")


    else:
        errors_dict = {"DATA":"Not a valid data"}
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS":getErrorMessage(errors_dict)}),
            content_type="application/json")


def queryset_to_dict(q_set):
    list_result = [entry for entry in q_set]
    return list_result

def get_da_details(request):

    if request.method == "POST":
        print("came rewwww")
        # print(request.POST["username"])
        user_obj = User.objects.get(username=request.POST["username"])
        user_profile = UserProfileInfo.objects.get(user=user_obj)
        da_profile = DaProfile.objects.get(user=user_profile)
        user_obj_s = serializers.serialize('json', [user_obj])
        user_profile_s = serializers.serialize('json', [user_profile])
        da_profile_s = serializers.serialize('json', [da_profile])
        return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"DATA FETCHED", "user_meta":user_obj_s, "da_profile":da_profile_s, "user_profile": user_profile_s}),
            content_type="application/json")

    else:
        errors_dict = {"DATA":"Not a valid data"}
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS":getErrorMessage(errors_dict)}),
            content_type="application/json")



# register delivery agent
def register(request):
    registered = False
    if request.method == "POST":

        print("came rewwww")
        print(request.POST["username"])


        is_create = True

        print("Pk "+request.POST["pk"])

        if(request.POST["pk"]):
            print("camepk")
            user = User.objects.get(pk=request.POST["pk"])
            is_create = False
            user_form = UserFormDa(request.POST, request.FILES, instance=user)

            profile = UserProfileInfo.objects.get(user=user)
            profile_form = UserProfileInfoFormDa(data=request.POST, instance=profile)

            da_profile = DaProfile.objects.get(user=profile)

            da_profile_form = DaProfileForm(request.POST, request.FILES, instance=da_profile)


        else:
            print("notcamepk")
            user_form = UserFormDa(request.POST, request.FILES)
            profile_form = UserProfileInfoFormDa(data=request.POST)
            da_profile_form = DaProfileForm(request.POST, request.FILES)

        # user_form = UserFormDa(request.POST, request.FILES)
        # profile_form = UserProfileInfoFormDa(data=request.POST)
        # da_profile_form = DaProfileForm(request.POST, request.FILES)




        if user_form.is_valid() and profile_form.is_valid() and da_profile_form.is_valid():

            user = user_form.save()

            if is_create :
                user.set_password(user.password)

            # else :
            #     print( "came updateaaaaaaa")
            #     user = User.objects.get(pk=request.POST["pk"])
            #     user = user_form.save()

            user = user_form.save()

            user.save()


            profile = profile_form.save(commit=False)

            if is_create:
                profile.user_type = dbconstants.USER_TYPE_DELIVERY_AGENT
                profile.slug = unique_slug_generator(profile)
                profile.ref_id = unique_ref_id_generator(profile)
                profile.user = user

            profile.location_state = request.POST["location_state"]



            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()



            da_profile = da_profile_form.save(commit=False)

            if is_create:
                da_profile.slug = unique_slug_generator(da_profile)

            da_profile.user = profile


            if 'rc_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['rc_pic']

            if 'pan_card_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['pan_card_pic']

            if 'driving_liscence_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['driving_liscence_pic']


            da_profile.save()

            registered = True

            if is_create :
                sucess_message = "Delivery Agent Registered successfully"
            else:
                sucess_message = "Delivery Agent Details updated successfully"

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":sucess_message}),
            content_type="application/json")
        else:
            print(user_form.errors, profile_form.errors)

            profile_form.errors.update(user_form.errors)
            profile_form.errors.update(da_profile_form.errors)
            errors_dict = Merge(user_form.errors, profile_form.errors)

            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": getErrorMessage(errors_dict)}),
            content_type="application/json")
    else:
        errors_dict = {"DATA":"Not a valid data"}
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS": errors_dict}),
            content_type="application/json")


@login_required
def order_create(request):
    registered = False
    print('order_craete_Came')
    if request.method == "POST":

        if not request.POST._mutable:
            request.POST._mutable = True

        post_data = request.POST;


        usernamet = request.POST["username"]
        post_data["first_name"] = usernamet
        post_data["username"] = usernamet.replace(" ", "")
        post_data["email"] = post_data["username"]+"@idelivery.com"
        post_data["password"] = post_data["username"]+"@123"
        post_data["phone_secondary"] = "0000000000"



        user_form = UserForm(data=post_data)
        profile_form = UserProfileInfoForm(data=request.POST)

        print("came create order 2")
        if user_form.is_valid() and profile_form.is_valid():
            print("came create order 3")
            profile_check = UserProfileInfo.objects.filter(phone_primary=post_data["phone_primary"], user_type = dbconstants.USER_TYPE_CONSUMER)

            proceed = True

            print(profile_check.count())


            if profile_check.count() == 0:
                user_parent_form = UserParentForm(data=post_data)
                if user_parent_form.is_valid():
                    print("kds")

                    print("came count 0")
                    print("came count "+post_data["username"])

                    profile = profile_form.save(commit=False)

                    profile.user_type = dbconstants.USER_TYPE_CONSUMER
                    profile.slug = unique_slug_generator(profile)
                    profile.ref_id = unique_ref_id_generator(profile)

                    user = user_parent_form.save()
                    user.set_password(user.password)
                    user.save()
                    profile.user = user
                else:
                    # profile_form.errors.update(user_form.errors)
                    # errors_dict = Merge(user_form.errors, profile_form.errors)
                    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": getErrorMessage(user_parent_form.errors)}),
                    content_type="application/json")


            else:
                print("came count 1")
                profile = profile_check[0]

                if(profile.user_status == dbconstants.USER_STATUS_ACTIVE):
                    user = User.objects.get(username = profile.user)
                    profile.user = user
                else:
                    return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS":"This user is disabled"}),
                    content_type="application/json")



            profile.phone_primary = post_data["phone_primary"]
            profile.phone_secondary = post_data["phone_secondary"]
            profile.location_sublocality = post_data["location_sublocality"]
            profile.location_area = post_data["location_area"]
            profile.location_locality = post_data["location_locality"]
            profile.location_city = post_data["location_city"]
            profile.location_pincode = post_data["location_pincode"]
            profile.location_state = post_data["location_state"]

            customer_location = post_data["location_area"] +", "+post_data["location_sublocality"]+", "+post_data["location_locality"]+", "+post_data["location_city"]+", "+post_data["location_pincode"]

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
            is_create = True

            if(request.POST["pk"]):
                is_create = False;
                order = Order.objects.get(order_id =request.POST["pk"])
                order_form = OrderForm(request.POST, instance= order)
            else:
                order_form = OrderForm(data=request.POST)


            if order_form.is_valid():

                order = order_form.save(commit=False)

                if is_create:
                    order.user_customer = profile
                    user_del = User.objects.get(username=post_data["user_delivery_agent"])
                    da_profile = UserProfileInfo.objects.get(user=user_del)
                    order.user_delivery_agent = da_profile
                    order.delivery_charges = 60
                    order.status_note = "Nothing to note"
                    order.slug = unique_slug_generator(order)
                    order.order_id = unique_order_id_generator(order)

                order.save()

                if is_create :
                    success_message = "Order Created successfully"
                else:
                    success_message = "Order updated successfully"



            else :
                return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": getErrorMessage(order_form.errors)}),
                content_type="application/json")



            # create order ends




            # create order item

            count_item_default = 2

            order_items = ". Items : "

            proceed_order_loop = True
            while proceed_order_loop:

                item_def = 'item_name_'+str(count_item_default)
                print("name_"+item_def)
                if item_def in post_data:
                    item_name = post_data["item_name_"+str(count_item_default)]
                    measurement_unit = post_data["measurement_unit_"+str(count_item_default)]
                    item_quantity =  post_data["item_quantity_"+str(count_item_default)]

                    print("came for=="+str(count_item_default))
                    order_item_model_form = OrderItemForm()


                    print("camess ss")
                    order_item_model =  OrderItem()
                    order_item_model.item_name = item_name
                    order_item_model.item_quantity = item_quantity
                    order_item_model.measurement_unit =   ItemMeasuementUnit.objects.get(name=measurement_unit)


                    if count_item_default > 1 :
                        order_items +=  ", "
                    order_items +=  item_name + " "+ item_quantity + " "+ measurement_unit

                    # order_item_model_form.save(commit=False)
                    order_item_model.slug = unique_slug_generator(order_item_model)
                    order_item_model.order_item_id = unique_order_item_id_generator(order_item_model)
                    order_item_model.measurement_unit = ItemMeasuementUnit.objects.get(name=measurement_unit)
                    order_item_model.order = order
                    count_item_default+=1
                    order_item_model.save()
                else :
                    proceed_order_loop = False

            # create order item ends

            # smsbase.sendOrderCreationMessage(customer_location = customer_location, order_number = order_model.order_id, order_items =order_items, customer_name = profile.user , customer_mobile = profile.phone_primary, da_name = user_del.username, da_mobile = da_profile.phone_primary)

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":success_message}),
            content_type="application/json")


        else:
            print(user_form.errors, profile_form.errors)

            profile_form.errors.update(user_form.errors)
            errors_dict = Merge(user_form.errors, profile_form.errors)

            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": getErrorMessage(errors_dict)}),
            content_type="application/json")
    else:
        errors_dict = {"Data":"Not a valid data"}
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS": errors_dict}),
        content_type="application/json")

# register customer_care agent
def register_customer_care(request):
    registered = False
    if request.method == "POST":

        print("came rewwww")
        print(request.POST["username"])


        is_create = True

        if(request.POST["pk"]):
            user = User.objects.get(pk=request.POST["pk"])
            is_create = False
            user_form = UserFormDa(request.POST, request.FILES, instance=user)

            profile = UserProfileInfo.objects.get(user=user)
            profile_form = UserProfileInfoFormDa(data=request.POST, instance=profile)

            da_profile = DaProfile.objects.get(user=profile)

            da_profile_form = DaProfileForm(request.POST, request.FILES, instance=da_profile)


        else:
            user_form = UserFormDa(request.POST, request.FILES)
            profile_form = UserProfileInfoFormDa(data=request.POST)
            da_profile_form = DaProfileForm(request.POST, request.FILES)

        # user_form = UserFormDa(request.POST, request.FILES)
        # profile_form = UserProfileInfoFormDa(data=request.POST)
        # da_profile_form = DaProfileForm(request.POST, request.FILES)




        if user_form.is_valid() and profile_form.is_valid() and da_profile_form.is_valid():

            user = user_form.save()

            if is_create :
                user.set_password(user.password)

            # else :
            #     print( "came updateaaaaaaa")
            #     user = User.objects.get(pk=request.POST["pk"])
            #     user = user_form.save()

            user = user_form.save()

            user.save()


            profile = profile_form.save(commit=False)

            if is_create:
                profile.user_type = dbconstants.USER_TYPE_CUSTOMER_CARE_EXECUTIVE
                profile.slug = unique_slug_generator(profile)
                profile.ref_id = unique_ref_id_generator(profile)
                profile.user = user

            profile.location_state = request.POST["location_state"]



            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()



            da_profile = da_profile_form.save(commit=False)

            if is_create:
                da_profile.slug = unique_slug_generator(da_profile)

            da_profile.user = profile


            if 'rc_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['rc_pic']

            if 'pan_card_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['pan_card_pic']

            if 'driving_liscence_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['driving_liscence_pic']


            da_profile.save()

            registered = True

            if is_create :
                sucess_message = "Customer Care Registered successfully"
            else:
                sucess_message = "Customer Care Details updated successfully"

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":sucess_message}),
            content_type="application/json")
        else:
            print(user_form.errors, profile_form.errors)

            profile_form.errors.update(user_form.errors)
            profile_form.errors.update(da_profile_form.errors)
            errors_dict = Merge(user_form.errors, profile_form.errors)

            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": getErrorMessage(errors_dict)}),
            content_type="application/json")
    else:
        errors_dict = {"DATA":"Not a valid data"}
        return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"INVALID DATA", "ERRORS": errors_dict}),
            content_type="application/json")

def getErrorMessage(errors_dict):
        err = next(iter(errors_dict))
        error_msg = errors_dict.get(err)
        error = str(err) + " : " + cleanhtml(error_msg)
        error = error.replace("_", " ")
        error = error.replace('""', "")
        # error = camelCase(error)

        return error

def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]

def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', str(raw_html))
  return cleantext
