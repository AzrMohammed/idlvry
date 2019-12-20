
// window.onload = function() {
//  alert("let's go!");
// }

function loginCheck (is_loggedin)
{

  // alert("Cakked== "+ is_loggedin);
// let d = new Date();
//    alert("Today's date is " + d);
  if(is_loggedin == 'True')
   {
     // alert("aa");
   }
  else
  {
      window.location.replace($('#login_url').val());
  // alert("aab");
  }


}


function deActivateUser(username)
{

var csrftoken = getCookie('csrftoken');

var url = $('#ul_user_status').val()

    $.ajax({
           type: "POST",
           url: url,
           headers: {"X-CSRFToken": csrftoken},
           data: {"username":username, "user_status":"AT"}, // serializes the form's elements.
           success: function(data)
           {
             // alert(JSON.stringify(data))
            // processResponse(data)

           }
         });



}

function activateUser(username)
{


  var csrftoken = getCookie('csrftoken');

  var url = $('#ul_user_status').val()

      $.ajax({
             type: "POST",
             url: url,
             headers: {"X-CSRFToken": csrftoken},
             data: {"username":username, "user_status":"UE"}, // serializes the form's elements.
             success: function(data)
             {
               // alert(JSON.stringify(data))
              // processResponse(data)

             }
           });


}

function proceedUserLogin()
{

  $('#error_el').text("");
  var form = $('#login_form');

  var formData = $(form).serialize();
  var url = form.attr('action');

      var username_v = $('#username').val();

      var password_v = $('#password').val()

      if(username_v == null || username_v === "")
      {
        $('#error_el').text("User Name not valid");
      }
      else if(password_v == null || password_v === "")
      {
        $('#error_el').text("Password not valid");
      }
      else
      $.ajax({
             type: "POST",
             url: url,
             data: form.serialize(), // serializes the form's elements.
             success: function(data)
             {
                 // alert(JSON.stringify(data)); // show response from the php script.

                 if(data.SUCCESS)
                  {
                    window.location.replace($('#login_success').val());
                    // alert(JSON.stringify(data))
                    // alert("successz"+data.RESPONSE_MESSAGE)

                  }
                 else
                 {
                   $('#error_el').text("Invalid Credentials");
                   // alert(JSON.stringify(data.ERRORS))
                 }

             }
           });
}

function proceedEdit(username)
{

is_edit = true;

// alert(username);

var csrftoken = getCookie('csrftoken');
$.ajax({
      type: "POST",
      url: $("#da_fetch").val(),
      headers: {"X-CSRFToken": csrftoken},
      // url: "/get_da_details/",
      data: {username:username}, // serializes the form's elements.
      success: function(data)
      {
        $('#registerBoy').modal('toggle');
          // alert(JSON.stringify(data)); // show response from the php script.
          if(data.SUCCESS)
           {

             alert(JSON.stringify(data))

             data_usermeta = JSON.parse(data.user_meta)[0]
             data_user_profile = JSON.parse(data.user_profile)[0]
             data_da_profile = JSON.parse(data.da_profile)[0]

             id_suffix = "";
             if(!(is_edit))
             id_suffix = "_v";
             // data_usermeta = data_json[0]
             alert(JSON.stringify(data_usermeta))

             $("#pk"+id_suffix).val(data_usermeta.pk)
             $("#username"+id_suffix).val(data_usermeta.fields.username)
             $("#first_name"+id_suffix).val(data_usermeta.fields.first_name)
             $("#email"+id_suffix).val(data_usermeta.fields.email)

             $("#phone_primary"+id_suffix).val(data_user_profile.fields.phone_primary)
             $("#phone_secondary"+id_suffix).val(data_user_profile.fields.phone_secondary)
             $("#location_area"+id_suffix).val(data_user_profile.fields.location_area)
             $("#location_sublocality"+id_suffix).val(data_user_profile.fields.location_sublocality)
             $("#location_locality"+id_suffix).val(data_user_profile.fields.location_locality)
             $("#location_city"+id_suffix).val(data_user_profile.fields.location_city)
             $("#location_pincode"+id_suffix).val(data_user_profile.fields.location_pincode)


             // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
             var server_prefix = $("#pic_server_prefix").val();
             // alert(server_prefix+data_user_profile.fields.profile_pic);


             var state_key = data_user_profile.fields.location_state;
             var state_key_val = "";

             var mapped_state = $('#location_state option').map(function() {
             var obj_state = {};
             obj_state[this.value] = this.textContent;
             if(state_key == this.value)
               state_key_val = this.textContent;
             return obj_state;
           });

// http://127.0.0.1:8000/media/

             $("#location_state"+id_suffix).val(state_key)


             $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
             $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
             $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
             $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);


             // $("#username_v").val(JSON.stringify(data))

           }
          else
          {
            alert(JSON.stringify(data.ERRORS))
          }

      }
    });


}

function proceedView(username)
{
  is_edit = false;



var csrftoken = getCookie('csrftoken');
$.ajax({
      type: "POST",
      url: $("#da_fetch").val(),
      headers: {"X-CSRFToken": csrftoken},
      // url: "/get_da_details/",
      data: {username:username}, // serializes the form's elements.
      success: function(data)
      {
        $('#registerBoyView').modal('toggle');
          // alert(JSON.stringify(data)); // show response from the php script.
          if(data.SUCCESS)
           {

             // alert(JSON.stringify(data))

             data_usermeta = JSON.parse(data.user_meta)[0]
             data_user_profile = JSON.parse(data.user_profile)[0]
             data_da_profile = JSON.parse(data.da_profile)[0]

             id_suffix = "";
             if(!(is_edit))
             id_suffix = "_v";
             // data_usermeta = data_json[0]
             // alert(JSON.stringify(data_usermeta))

             $("#pk"+id_suffix).val(data_usermeta.pk)
             $("#username"+id_suffix).text(data_usermeta.fields.username)
             $("#first_name"+id_suffix).text(data_usermeta.fields.first_name)
             $("#email"+id_suffix).text(data_usermeta.fields.email)

             $("#phone_primary"+id_suffix).text(data_user_profile.fields.phone_primary)
             $("#phone_secondary"+id_suffix).text(data_user_profile.fields.phone_secondary)
             $("#location_area"+id_suffix).text(data_user_profile.fields.location_area)
             $("#location_sublocality"+id_suffix).text(data_user_profile.fields.location_sublocality)
             $("#location_locality"+id_suffix).text(data_user_profile.fields.location_locality)
             $("#location_city"+id_suffix).text(data_user_profile.fields.location_city)
             $("#location_pincode"+id_suffix).text(data_user_profile.fields.location_pincode)


             // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
             var server_prefix = $("#pic_server_prefix").val();
             // alert(server_prefix+data_user_profile.fields.profile_pic);


             var state_key = data_user_profile.fields.location_state;
             var state_key_val = "";

             var mapped_state = $('#location_state option').map(function() {
             var obj_state = {};
             obj_state[this.value] = this.textContent;
             if(state_key == this.value)
               state_key_val = this.textContent;
             return obj_state;
           });


// http://127.0.0.1:8000/media/

             $("#location_state"+id_suffix).val(state_key_val)


             $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
             $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
             $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
             $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);


             // $("#username_v").val(JSON.stringify(data))

           }
          else
          {
            // alert(JSON.stringify(data.ERRORS))
          }

      }
    });

}





function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


function registerCustomerCare() {
var form = $('#register_customer_care_form');

var formData = $(form).serialize();
var url = form.attr('action');

 $('#error_el').val("")
 $('#success_el').val("")

    $.ajax({
           type: "POST",
           url: url,
           enctype:"multipart/form-data",
           data: new FormData(document.getElementById("register_customer_care_form")), // serializes the form's elements.
           processData: false,
           contentType: false,
           success: function(data)
           {
               // alert(JSON.stringify(data)); // show response from the php script.
               processResponse(data)

           }
         });

}

function registerAgent() {
var form = $('#register_agent_form');

var formData = $(form).serialize();
var url = form.attr('action');

 $('#error_el').val("")
 $('#success_el').val("")

    $.ajax({
           type: "POST",
           url: url,
           enctype:"multipart/form-data",
           data: new FormData(document.getElementById("register_agent_form")), // serializes the form's elements.
           processData: false,
           contentType: false,
           success: function(data)
           {
               // alert(JSON.stringify(data)); // show response from the php script.
               processResponse(data)

           }
         });

}



function processResponse(data)
{
  if(data.SUCCESS)
   {
     // alert(JSON.stringify(data))
   $('#success_el').text(data.RESPONSE_MESSAGE)

   $('#register_agent_form').trigger("reset");
   window.setTimeout( location.reload(), 4000 );
   ;
     // alert("success"+data.RESPONSE_MESSAGE)
   }
  else
  {


    // alert(JSON.stringify(data.ERRORS))
    $('#error_el').text(data.ERRORS)

  }
}

function createOrder()
{
  var form = $('#create_order_form');

  var formData = $(form).serialize();
  var url = form.attr('action');
  // alert(JSON.stringify(formData));

      $.ajax({
             type: "POST",
             url: url,

             data: form.serialize(), // serializes the form's elements.
             success: function(data)
             {
               alert(JSON.stringify(data))
              // processResponse(data)

             }
           });

}


function openDaRegisterForm()
{
  $('#registerBoy').modal('toggle');

  var id_suffix = "";

  $("#profile_pic_v"+id_suffix).hide()
  $("#driving_liscence_pic_v"+id_suffix).hide()
  $("#pan_card_pic_v"+id_suffix).hide()
  $("#rc_pic_v"+id_suffix).hide()




}


function openDaRegisterCustomerCareForm()
{
  $('#registerBoy').modal('toggle');

  var id_suffix = "";

  $("#profile_pic_v"+id_suffix).hide()
  $("#driving_liscence_pic_v"+id_suffix).hide()
  $("#pan_card_pic_v"+id_suffix).hide()
  $("#rc_pic_v"+id_suffix).hide()




}

function getOrderDetails()
{

 var csrftoken = getCookie('csrftoken');
 $.ajax({
        type: "POST",
        url: $("#order_fetch").val(),
        headers: {"X-CSRFToken": csrftoken},
        // url: "/get_da_details/",
        data: {order_id:'O19DLGRG'}, // serializes the form's elements.
        success: function(data)
        {
          $('#create_order_form_parent').modal('toggle');
            // alert(JSON.stringify(data)); // show response from the php script.
            if(data.SUCCESS)
             {

               alert(JSON.stringify(data))
               final_data = JSON.parse(JSON.stringify(data))
               response_message = final_data.RESPONSE_MESSAGE
               data_order_meta = final_data.order_meta
               data_customer_meta = final_data.user_customer.meta
               data_customer_profile = final_data.user_customer.profile[0]
               data_delivery_agent_meta = final_data.user_delivery_agent.meta
               data_delivery_agent_profile = final_data.user_delivery_agent.profile[0]




               $("#item_name").val(JSON.stringify(data))

               $("#username").val(data_customer_meta['username']);
               $("#phone_primary").val(data_customer_profile['phone_primary'])
               $("#location_city").val(data_customer_profile['location_city'])
               $("#location_locality").val(data_customer_profile['location_locality'])
               $("#location_area").val(data_customer_profile['location_area'])
               $("#location_sublocality").val(data_customer_profile['location_sublocality'])
               $("#location_pincode").val(data_customer_profile['location_pincode'])
               $("#location_state").val(data_customer_profile['location_pincode'])

               var state_key = data_customer_profile['location_state'];
               var state_key_val = "";
               console.log(state_key);

               var mapped_state = $('#location_state option').map(function() {
               var obj_state = {};
               obj_state[this.value] = this.textContent;
               // alert("came opt"+this.value)
               if(state_key == this.value)
                 {
                   // alert("came opts=="+this.value)
                   state_key_val = this.value;
                 }
               return obj_state;
             });


  // http://127.0.0.1:8000/media/

              // alert("Selected val==="+state_key_val+"==")

               $("#location_state").val(state_key_val)




               // $("#first_name"+id_suffix).val(data_usermeta.fields.first_name)


             }
            else
            {
              alert(JSON.stringify(data.ERRORS))
            }

        }
      });

}

function getDaDetails()
{
   // var csrftoken = document.cookie
   // print(csrftoken)
   // getCookie('csrftoken');
   var csrftoken = getCookie('csrftoken');
  $.ajax({
         type: "POST",
         url: $("#da_fetch").val(),
         headers: {"X-CSRFToken": csrftoken},
         // url: "/get_da_details/",
         data: {username:"Banu"}, // serializes the form's elements.
         success: function(data)
         {
           $('#registerBoyView').modal('toggle');
             // alert(JSON.stringify(data)); // show response from the php script.
             if(data.SUCCESS)
              {

                alert(JSON.stringify(data))

                data_usermeta = JSON.parse(data.user_meta)[0]
                data_user_profile = JSON.parse(data.user_profile)[0]
                data_da_profile = JSON.parse(data.da_profile)[0]

                id_suffix = "";
                if(!(is_edit))
                id_suffix = "_v";
                // data_usermeta = data_json[0]
                // alert(JSON.stringify(data_usermeta))

                $("#pk"+id_suffix).val(data_usermeta.pk)
                $("#username"+id_suffix).val(data_usermeta.fields.username)
                $("#first_name"+id_suffix).val(data_usermeta.fields.first_name)
                $("#email"+id_suffix).val(data_usermeta.fields.email)

                $("#phone_primary"+id_suffix).val(data_user_profile.fields.phone_primary)
                $("#phone_secondary"+id_suffix).val(data_user_profile.fields.phone_secondary)
                $("#location_area"+id_suffix).val(data_user_profile.fields.location_area)
                $("#location_sublocality"+id_suffix).val(data_user_profile.fields.location_sublocality)
                $("#location_locality"+id_suffix).val(data_user_profile.fields.location_locality)
                $("#location_city"+id_suffix).val(data_user_profile.fields.location_city)
                $("#location_pincode"+id_suffix).val(data_user_profile.fields.location_pincode)


                // $("#profile_pic_v").src(data_user_profile.fields.profile_pic)
                var server_prefix = $("#pic_server_prefix").val();
                // alert(server_prefix+data_user_profile.fields.profile_pic);


                var state_key = data_user_profile.fields.location_state;
                var state_key_val = "";

                var mapped_state = $('#location_state option').map(function() {
                var obj_state = {};
                obj_state[this.value] = this.textContent;
                if(state_key == this.value)
                  state_key_val = this.textContent;
                return obj_state;
              });

// http://127.0.0.1:8000/media/

                $("#location_state"+id_suffix).val(state_key_val)


                $("#profile_pic_v"+id_suffix).attr("src",  server_prefix+data_user_profile.fields.profile_pic);
                $("#driving_liscence_pic_v"+id_suffix).attr("src",  server_prefix+data_da_profile.fields.driving_liscence_pic);
                $("#pan_card_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.pan_card_pic);
                $("#rc_pic_v"+id_suffix).attr("src", server_prefix+data_da_profile.fields.rc_pic);



              }
             else
             {
               // alert(JSON.stringify(data.ERRORS))
             }

         }
       });

}






function getOrderItemComponent()
{


  var count_order_items = $("#ole li").length;
  alert(count_order_items);
  var current_index = count_order_items+1;

  var html_content = '<li>';
  html_content += '<div class="form-group col-md-8 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">1. Items name / product name (ಉತ್ಪನ್ನದ ಹೆಸರು)</label>';
  html_content += '<input type="text" class="form-control" id="item_name" name="item_name_'+current_index+'" placeholder="Write down the requirment">';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="exampleInputEmail1">Quantity</label>';
  html_content += '<input type="number" class="form-control" id="item_quantity" value="1" name="item_quantity_'+current_index+'" placeholder="Quantity">';
  html_content += '</div>';
  html_content += '<div class="form-group col-md-2 pl_0 float-left">';
  html_content += '<label for="">UNIT</label>';
  html_content += '<select class="form-control" id="measurement_unit" name="measurement_unit_'+current_index+'">';
  var cont = document.getElementById("measurement_unit").innerHTML;
  html_content += cont;
  html_content += '</select>';
  html_content += '</div>';
  html_content += '</li>';

   $("#ole").append(html_content);

}
