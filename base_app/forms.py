from django import forms
from django.contrib.auth.models import User
from base_app.models import UserProfileInfo, Order, OrderItem, DaProfile
from base_app import dbconstants


class UserParentForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        # exclude = ['username']

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
        exclude = ['username']

class UserFormDa(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'first_name', 'email', 'password')



class UserProfileInfoForm(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('phone_primary', 'phone_secondary', 'location_area','location_sublocality','location_locality','location_city','location_pincode','profile_pic')


class UserProfileInfoFormDa(forms.ModelForm):

    class Meta():
        model = UserProfileInfo
        fields = ('phone_primary', 'phone_secondary', 'location_area','location_sublocality','location_locality','location_city','location_pincode', 'profile_pic')

    def __init__(self, *args, **kwargs):
        super(UserProfileInfoFormDa, self).__init__(*args, **kwargs)
        self.fields['location_locality'].required = False
        self.fields['phone_secondary'].required = False

class DaProfileForm(forms.ModelForm):
    class Meta():
        model = DaProfile
        fields = ('user', 'driving_liscence_pic', 'pan_card_pic','rc_pic')

    def __init__(self, *args, **kwargs):
        super(DaProfileForm, self).__init__(*args, **kwargs)
        self.fields['user'].required = False
        self.fields['pan_card_pic'].required = False
        self.fields['rc_pic'].required = False

class OrderForm(forms.Form):
    # class Meta():
    #     model = Order
    #     fields = ('user_delivery_agent', 'delivery_charges', 'status_note')

    customer_name = forms.CharField(label='Customer Name', max_length=50)
    phone_primary = forms.CharField(max_length=10, label='Phone Number' )
    location_sublocality = forms.CharField(max_length=80, label='Address' )
    location_locality = forms.CharField(max_length=80, label='Locality')
    location_city = forms.CharField(max_length=80,  label='City')
    # location_state = models.CharField(max_length=80, unique=False, default="KERALA")
    location_pincode = forms.CharField(max_length=6, label='Pincode')
    delivery_agent = forms.ModelChoiceField(queryset=UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT))
    # UserProfileInfo.objects.prefetch_related('user').filter(user_type = dbconstants.USER_TYPE_DELIVERY_AGENT)
    # forms.ModelChoiceField(queryset=User.objects.all().order_by('username'))
    # forms.CharField(max_length=80,  label='Delivery Agent')



class OrderItemForm(forms.ModelForm):

    class Meta():
        model = OrderItem
        fields = ('measurement_unit', 'item_name', 'item_quantity')
        exclude = ['measurement_unit']
