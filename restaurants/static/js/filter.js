// Wait for the document to be fully loaded
document.addEventListener("DOMContentLoaded", function() {
  // Get references to the filter button and all the checkboxes
  var filterButton = document.getElementById("filter-button");
  var scoreCheckboxes = document.querySelectorAll('input[type="checkbox"][data-category-id]');

  // Add a click event listener to the filter button
  filterButton.addEventListener("click", function() {
    // Create an array to store the selected scores
    var selectedScores = [];

    // Loop through the score checkboxes and check which ones are selected
    scoreCheckboxes.forEach(function(checkbox) {
      if (checkbox.checked) {
        selectedScores.push(checkbox.nextElementSibling.textContent.trim());
      }
    });

    // Get all the restaurant strips
    var restaurantStrips = document.querySelectorAll('.strip');

    // Loop through the restaurant strips and hide/show them based on the selected scores
    restaurantStrips.forEach(function(restaurantStrip) {
      var restaurantScore = parseInt(restaurantStrip.querySelector('.score strong').textContent);

      // If no scores are selected, show all restaurants
      if (selectedScores.length === 0) {
        restaurantStrip.style.display = 'block';
      } else {
        // If the restaurant's score is in the selected scores array, show it; otherwise, hide it
        if (selectedScores.includes(restaurantScore.toString())) {
          restaurantStrip.style.display = 'block';
        } else {
          restaurantStrip.style.display = 'none';
        }
      }
    });
  });
});
