document.addEventListener("DOMContentLoaded", function() {
    var filterButton = document.getElementById("filter-button");

    filterButton.addEventListener("click", function() {
        var selectedCategories = document.querySelectorAll('.category-checkbox:checked');
        var selectedScores = document.querySelectorAll('.score-checkbox:checked');
        var restaurantDivs = document.querySelectorAll('#restaurant-list .col-xl-4, #restaurant-list .col-lg-6, #restaurant-list .col-md-6, #restaurant-list .col-sm-6');

        restaurantDivs.forEach(function(div) {
            var restaurantStrip = div.querySelector('.strip');
            var category = restaurantStrip.getAttribute('data-category');
            var score = parseFloat(restaurantStrip.getAttribute('data-score'));

            var showRestaurant = true;

            // Check category filter
            if (selectedCategories.length > 0) {
                showRestaurant = Array.from(selectedCategories).some(function(checkbox) {
                    return checkbox.getAttribute('data-category-name') === category;
                });
            }

            // Check score filter
            if (selectedScores.length > 0) {
                showRestaurant = showRestaurant && Array.from(selectedScores).some(function(checkbox) {
                    return score >= parseFloat(checkbox.value);
                });
            }

            div.style.display = showRestaurant ? '' : 'none';
        });
    });
});
