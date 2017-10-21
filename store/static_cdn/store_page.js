$('.buy-btn').click(function () {
    console.log(this.getAttribute('data'));
    $.ajax({
        url: "/add/",
        data: {'id': this.getAttribute('data')},
        dataType: 'json',
        success: function (data) {
            if (data.get('is_added') === "success") {
                $('.bucket-btn').value = $('.bucket-btn').value + 1
            }
        }
    }).done(function (data) {
        console.log(data)
    });
});