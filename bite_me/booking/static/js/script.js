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
