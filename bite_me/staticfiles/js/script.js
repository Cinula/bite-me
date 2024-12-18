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

// Menu search functionality
document.addEventListener('DOMContentLoaded', function () {
    const searchForm = document.getElementById('menuSearchForm');
    const searchInput = document.getElementById('menuSearch');

    if (searchForm && searchInput) {
        searchInput.addEventListener('input', function (e) {
            const searchTerm = e.target.value.toLowerCase();
            const menuItems = document.querySelectorAll('.menu-item-card');

            menuItems.forEach(item => {
                const title = item.querySelector('.card-title').textContent.toLowerCase();
                const description = item.querySelector('.card-text').textContent.toLowerCase();

                if (title.includes(searchTerm) || description.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });

        searchForm.addEventListener('submit', function (e) {
            e.preventDefault();
        });
    }
});

// Booking form date restrictions
document.addEventListener('DOMContentLoaded', function () {
    const dateInput = document.querySelector('input[type="date"]');
    if (dateInput) {
        // Set min date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);

        // Set max date to 30 days from now
        const maxDate = new Date();
        maxDate.setDate(maxDate.getDate() + 30);
        dateInput.setAttribute('max', maxDate.toISOString().split('T')[0]);

        // If no date is selected, default to today
        if (!dateInput.value) {
            dateInput.value = today;
        }
    }
});
