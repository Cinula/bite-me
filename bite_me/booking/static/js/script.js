/* booking/static/js/script.js */

// Automatically fade out flash messages after 5 seconds
$(document).ready(function () {
    setTimeout(function () {
        $(".alert").alert('close');
    }, 5000);
});
