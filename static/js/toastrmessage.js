document.addEventListener('DOMContentLoaded', function () {
    var messages = document.querySelectorAll('#django-messages .message');
    toastr.options = {
        "closeButton": true,
        "progressBar": true,
        "timeOut": "3000",
        "positionClass": "toast-top-right"
    };

    messages.forEach(function (msg) {
        var type = msg.getAttribute('data-type');
        var text = msg.textContent || msg.innerText;
        toastr[type](text);
    });
});
