
$(document).ready(function(){
  $(".notification-toggle").click(function(e){
    e.preventDefault();
    $.ajax({
      type: "POST",
      url: "{% url 'get_notifications_ajax' %}",
      data: {
        csrfmiddlewaretoken: "{{ csrf_token }}",
      },
      success: function(data){
        $("#notification_dropdown").html(' <li role="presentation" class="dropdown-header">Notifications</li>');
        var count = data.count
        if (count == 0) {
          var url = '{% url "notifications:all" %}'
          $("#notification_dropdown").append("<li><a href='" + '{% url 'all_Read' %}' + "'>View All Notifications</a></li>")
        } else {
          $(data.notifications).each(function(){
            var link = this;
            $("#notification_dropdown").append("<li><a href='" + '{% url 'all_Read' %}' + "'>" + link + "</li>")

          })
        }
        console.log(data.notifications);

      },
      error: function(rs, e) {
        console.log(rs);
        console.log(e);
      }

    })

  })

})
