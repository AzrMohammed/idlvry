import requests


# auth_key = 304757AYVqJYJdk54G5dd4ce8e
# https://api.msg91.com/api/sendhttp.php?route=4&sender=TESTIN&message=Hello!%20This%20is%20a%20test%20message&country=91&mobiles=9080349072&authkey=304757AYVqJYJdk54G5dd4ce8e


def sendOrderCreationMessage(**kwargs):

    for key, value in kwargs.items():
        print("The value of {} is {}".format(key, value))

    print(kwargs.get("order_number"))
# (order_number = order_model.order_id, order_items = "Shampoo, Rice", customer_name = profile.user ,
 # customer_mobile = profile.phone_primary, da_name = user_del.username, da_mobile = da_profile.phone_primary)
    base_url = "https://api.msg91.com/api/sendhttp.php?route=4&sender=IDLVRY&country=91&authkey=304757AYVqJYJdk54G5dd4ce8e"
    # customer_name = "Aiyappa"
    # customer_mobile = "9080349072"
    # da_name = "Da1"
    # da_mobile = "9080349072"
    #
    # message_customer = "Hi "+customer_name+" your order (Id: HIBNKSQ4S) has been placed, Delivery agent is on his way for pickup items."




    message_customer = "Hi "+str(kwargs.get("customer_name"))+", your order has been placed with order id ( "+ kwargs.get("order_number") +" ) . Delivery agent ( "+ kwargs.get("da_name") +" "+kwargs.get("da_mobile")+" ) is on his way to pick up the order.\nThank you."
    message_da = "Order no."+str(kwargs.get("order_number"))+" has been assigned to you for "+str(kwargs.get("customer_name"))+ " "+ str(kwargs.get("customer_mobile"))+ " " +str(kwargs.get("order_items"))+ "to be delivered at "+str(kwargs.get("customer_location"))+"."
    url_da = base_url+"&message="+message_da+"&mobiles="+kwargs.get("da_mobile")
    url_customer = base_url+"&message="+message_customer+"&mobiles="+kwargs.get("customer_mobile")
    print(url_customer)
    print(url_da)
    r_customer = requests.get(url_customer)
    r_da = requests.get(url_da)

    print(str(r_customer))
    print(str(r_da))
