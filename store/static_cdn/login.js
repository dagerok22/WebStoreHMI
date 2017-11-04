$(function () {

    $('#login-form-link').click(function (e) {
        $("#login-form").delay(100).fadeIn(100);
        $("#register-form").fadeOut(100);
        $('#register-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });
    $('#register-form-link').click(function (e) {
        $("#register-form").delay(100).fadeIn(100);
        $("#login-form").fadeOut(100);
        $('#login-form-link').removeClass('active');
        $(this).addClass('active');
        e.preventDefault();
    });

    console.log("here")
    $('#register-username').addEventListener('change',function (e) {
        console.log(this.value)
        alert("")
    //     $.ajax({
    //     url: "/add/",
    //     data: {'id': this.getAttribute('data')},
    //     dataType: 'json',
    //     success: function (data) {
    //         if (data.get('is_added') === "success") {
    //             $('.bucket-btn').value = $('.bucket-btn').value + 1
    //         }
    //     }
    // }).done(function (data) {
    //     console.log(data)
    // });
    })

});
