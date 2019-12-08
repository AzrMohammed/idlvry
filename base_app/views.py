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

    base_dict = {"order_count":order_count, "delivery_boy_count":delivery_boy_count, "order_delivered":order_delivered_count, "customers_count":customers_count, "delivery_agents":users, 'pic_server_prefix':'http://127.0.0.1:8000/media/' }
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
    return render(request, 'base_app/delivery_agents.html',  {'state_list':dbconstants.STATE_LIST_DICT, 'users': users, 'pic_server_prefix':'http://127.0.0.1:8000/media/' })

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
        # print("sizeaaa:"+ str(order_items.count()))

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

        user = authenticate(request, username = username, password = password)

        if user:
            if user.is_active:
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
            return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"3INVALID DATA", "ERRORS": errors_dict}),
            content_type="application/json")

    else:
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






@login_required
def order_create(request):
    registered = False
    if request.method == "POST":

        if not request.POST._mutable:
            request.POST._mutable = True

        post_data = request.POST;
        print("came create order 3")
        print("came create order" +str(post_data))



        post_data["first_name"] = request.POST["username"]
        post_data["email"] = request.POST["username"]+"@idelivery.com"
        post_data["password"] = request.POST["username"]+"@123"
        post_data["phone_secondary"] = "0000000000"

        user_form = UserForm(data=post_data)
        profile_form = UserProfileInfoForm(data=request.POST)

        print("came create order 2")
        if user_form.is_valid() and profile_form.is_valid():
            print("came create order 3")
            profile_check = UserProfileInfo.objects.filter(phone_primary=post_data["phone_primary"], user_type = dbconstants.USER_TYPE_CONSUMER)

            proceed = True

            if profile_check.count() == 0:
                user_parent_form = UserParentForm(data=post_data)
                if user_parent_form.is_valid():

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

            # create order

            order_model = Order()

            order_model.user_customer = profile

            user_del = User.objects.get(username=post_data["user_delivery_agent"])

            da_profile = UserProfileInfo.objects.get(user=user_del)

            order_model.user_delivery_agent = da_profile
            order_model.delivery_charges = 60
            order_model.status_note = "Nothing to note"

            order_model.slug = unique_slug_generator(order_model)
            order_model.order_id = unique_order_id_generator(order_model)

            order_model.save()

            # create order ends


            # create order item


            item_name_list = request.POST.getlist("item_name")
            measurement_unit_list = request.POST.getlist("measurement_unit")
            item_quantity_list = request.POST.getlist("item_quantity")

            print("sampled"+measurement_unit_list[0])
            print("sampledaw"+str(len(item_name_list)))

            order_items = ". Items : "
            item_count = len(item_name_list)
            i=0
            # order_
            while i<item_count :

                print("came for=="+str(i))
                order_item_model_form = OrderItemForm()

                print("mmunit :"+post_data["measurement_unit"])
                # order_item_model_form.item_name = item_name_list[i]
                # order_item_model_form.item_quantity = item_quantity_list[i]
                # order_item_model_form.measurement_unit =   ItemMeasuementUnit.objects.get(name=measurement_unit_list[i])

                # if order_item_model_form.is_valid():
                print("camess ss")
                order_item_model =  OrderItem()
                order_item_model.item_name = item_name_list[i]
                order_item_model.item_quantity = item_quantity_list[i]
                order_item_model.measurement_unit =   ItemMeasuementUnit.objects.get(name=measurement_unit_list[i])


                if i > 0 :
                    order_items +=  ", "
                order_items +=  item_name_list[i] + " "+ item_quantity_list[i]+ " "+ measurement_unit_list[i]

                # order_item_model_form.save(commit=False)
                order_item_model.slug = unique_slug_generator(order_item_model)
                order_item_model.order_item_id = unique_order_item_id_generator(order_item_model)
                order_item_model.measurement_unit = ItemMeasuementUnit.objects.get(name=measurement_unit_list[i])
                order_item_model.order = order_model
                i+=1
                order_item_model.save()
                # else:
                #     print("camess no")
                #     i+=1
                #     errors_dict = order_item_model_form.errors
                #     return HttpResponse(json.dumps({"SUCCESS":False, "RESPONSE_MESSAGE":"ERRORS", "ERRORS": errors_dict}),
                #     content_type="application/json")



            # create order item ends

            smsbase.sendOrderCreationMessage(customer_location = customer_location, order_number = order_model.order_id, order_items =order_items, customer_name = profile.user , customer_mobile = profile.phone_primary, da_name = user_del.username, da_mobile = da_profile.phone_primary)

            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Order Created"}),
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

#
# def grouped(iterable, n):
#     return izip(*[iter(iterable)]*n)


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

        if(request.POST["pk"]):
            is_create = False


        # print("aaaaaa registur is create "+ str(is_create))

        # for filename, file in request.FILES.iteritems():
            # name = request.FILES[filename].name

        user_form = UserFormDa(request.POST, request.FILES)
        profile_form = UserProfileInfoFormDa(data=request.POST)
        da_profile_form = DaProfileForm(request.POST, request.FILES)




        if user_form.is_valid() and profile_form.is_valid() and da_profile_form.is_valid():


            if is_create :
                print( "came createaaaaaaa")
                user = user_form.save()
                user.set_password(user.password)
            else :
                print( "came updateaaaaaaa")
                user = User.objects.get(pk=request.POST["pk"])
                user = user_form.save()


            user.save()



            if is_create:
                profile = profile_form.save(commit=False)
                profile.user_type = dbconstants.USER_TYPE_DELIVERY_AGENT
                profile.slug = unique_slug_generator(profile)
                profile.ref_id = unique_ref_id_generator(profile)
                profile.user = user
            else:

                profile = UserProfileInfo.objects.get(user=user)
                profile = profile_form.save(commit=False)

            profile.location_state = request.POST["location_state"]



            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()



            if is_create:
                da_profile = da_profile_form.save(commit=False)
                da_profile.slug = unique_slug_generator(da_profile)
                da_profile.user = profile
            else:
                da_profile = DaProfile.objects.get(user=profile)
                da_profile = da_profile_form.save(commit=False)


            if 'rc_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['rc_pic']

            if 'pan_card_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['pan_card_pic']

            if 'driving_liscence_pic' in request.FILES:
                da_profile.rc_pic = request.FILES['driving_liscence_pic']


            da_profile.save()

            registered = True
            return HttpResponse(json.dumps({"SUCCESS":True, "RESPONSE_MESSAGE":"Delivery Agent Registered successfully"}),
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
