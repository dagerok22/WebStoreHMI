
$('.buy-btn').click(function () {
    console.log(this.getAttribute('data'));
    $.ajax({
        url: "/add/",
        data: {'id':this.getAttribute('data')},
        dataType: 'json',
        success: function (data) {
          if (data) {
            alert(data);
          }
        }
    }).done(function (data) {
        console.log(data)
    });
});