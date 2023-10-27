document.addEventListener("DOMContentLoaded", function() {
    var filterButton = document.getElementById("filter-button");

    filterButton.addEventListener("click", function() {
        // Get selected category options
        var selectedCategories = document.querySelectorAll('.category-checkbox:checked');

        var restaurantStrips = document.querySelectorAll('.strip');

        console.log("Selected Categories:", selectedCategories);

        restaurantStrips.forEach(function(restaurantStrip) {
            var category = restaurantStrip.getAttribute('data-category');
            console.log("Restaurant Category:", category);
            var score = parseFloat(restaurantStrip.getAttribute('data-score'));

            console.log("Show Restaurant:", showRestaurant);

            var showRestaurant = false;

            if (selectedCategories.length === 0) {
                showRestaurant = true;
            } else {
                selectedCategories.forEach(function(checkbox) {
                    if (checkbox.checked) {
                        var selectedCategoryName = checkbox.getAttribute('data-category-name');
                        if (selectedCategoryName === category) {
                            showRestaurant = true;
                        }
                    }
                });
            }

            restaurantStrip.style.display = showRestaurant ? 'block' : 'none';
        });
    });
});
