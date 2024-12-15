// Automatically fade out flash messages after 5 seconds
$(document).ready(function () {
    setTimeout(function () {
        $(".alert").alert('close');
    }, 5000);

    // Menu Search Functionality
    $('#menuSearch').on('keyup', function () {
        var value = $(this).val().toLowerCase();
        $('.menu-item-card').filter(function () {
            $(this).toggle($(this).find('.card-title').text().toLowerCase().indexOf(value) > -1)
        });
    });
});
