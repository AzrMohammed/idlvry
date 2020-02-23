from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from base_app import dbconstants
from django.contrib.auth.models import AbstractUser
# from phonenumber_field.modelfields import PhoneNumberField


# ./manage.py migrate base_app zero
class UserProfileInfo(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True)

    slug = models.SlugField(unique=True, max_length=8)
    ref_id = models.CharField(max_length=15, unique=True)

    phone_primary = models.CharField(max_length=10, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    phone_secondary = models.CharField(max_length=10, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_area = models.CharField(max_length=80, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_sublocality = models.CharField(max_length=80, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_locality = models.CharField(max_length=80, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_city = models.CharField(max_length=80, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    location_state = models.CharField(max_length=80, unique=False, choices=dbconstants.STATE_LIST, default=dbconstants.STATE_KARNATAKA)
    location_pincode = models.CharField(max_length=6, unique=False, default=dbconstants.VAL_STR_DEFAULT)
    user_type = models.CharField(max_length=3, choices=dbconstants.USER_TYPES, default = dbconstants.USER_TYPE_DELIVERY_AGENT)

    user_status = models.CharField(max_length=2, choices=dbconstants.USER_STATUS, default=dbconstants.USER_STATUS_ACTIVE)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def getProfilePic(self):
        return str(self.user.profile_pic)


    def __str__(self):
        return str(self.user.username)

class DaProfile(models.Model):
    slug = models.SlugField(unique=True, max_length=8)

    user = models.ForeignKey(UserProfileInfo, limit_choices_to={'user_type': dbconstants.USER_TYPE_DELIVERY_AGENT}, related_name='da_proofs', on_delete=models.CASCADE)
    driving_liscence_pic = models.ImageField(upload_to='proof_details', blank=True)
    pan_card_pic = models.ImageField(upload_to='proof_details', blank=True)
    rc_pic = models.ImageField(upload_to='proof_details', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)


class Business(models.Model):

    slug = models.SlugField(unique=True, max_length=8)
    user = models.ForeignKey(UserProfileInfo, limit_choices_to={'user_type': dbconstants.USER_TYPE_BUSINESS_OWNER}, related_name='user_business', on_delete=models.CASCADE)
    business_nature = models.CharField(max_length=100)
    status = models.CharField(max_length=2, choices=dbconstants.BUSINESS_STORE_STATUS, default=dbconstants.BUSINESS_STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.slug)


class ItemMeasuementUnit(models.Model):

    slug = models.SlugField(unique=True, max_length=8)
    name = models.CharField(max_length=50, default=dbconstants.VAL_STR_DEFAULT, null=True)
    note = models.CharField(max_length=250)
    status = models.CharField(max_length=2, choices=dbconstants.STATUS,  default=dbconstants.STATUS_ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.name)





class Order(models.Model):


    slug = models.SlugField(unique=True, max_length=8)
    order_id = models.CharField(max_length=15, unique=True)
    user_customer = models.ForeignKey(UserProfileInfo, limit_choices_to={'user_type': dbconstants.USER_TYPE_CONSUMER}, related_name='user_customer', on_delete=models.CASCADE)
    user_delivery_agent = models.ForeignKey(UserProfileInfo, limit_choices_to={'user_type': dbconstants.USER_TYPE_DELIVERY_AGENT},  related_name='user_delivery_agent', on_delete=models.CASCADE)
    delivery_charges = models.FloatField(max_length=5, default=1.0)
    status_note = models.CharField(max_length=200, default=dbconstants.VAL_STR_DEFAULT, null=True)
    status = models.CharField(max_length=3, choices=dbconstants.ORDER_STATUS,  default=dbconstants.ORDER_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.order_id)



class OrderEvent(models.Model):
    slug = models.SlugField(unique=True, max_length=8)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status_note = models.CharField(max_length=200, default=dbconstants.VAL_STR_DEFAULT, null=True)
    status = models.CharField(max_length=3, choices=dbconstants.ORDER_EVENT_STATUS,  default=dbconstants.ORDER_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class OrderItem(models.Model):

    slug = models.SlugField(unique=True, max_length=8)
    order_item_id = models.CharField(max_length=15, unique=True)
    item_name = models.CharField(max_length=60)
    item_quantity = models.PositiveSmallIntegerField(default=1)
    item_price = models.FloatField(max_length=5, default=1.0)
    status_note = models.CharField(max_length=200, unique=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    measurement_unit = models.ForeignKey(ItemMeasuementUnit, related_name='measurement_unit', on_delete=models.CASCADE, default="", unique=False)
    status = models.CharField(max_length=3, choices=dbconstants.O_ITEM_STATUS, default=dbconstants.O_ITEM_PLACED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.order_item_id)
