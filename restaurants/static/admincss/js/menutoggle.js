// ADD TO MENU SAYFASI 
// ürün silme ve visibility toggleları


function deleteItem(itemId) {
    // silme
    fetch(`/delete-item/${itemId}/`, {
      method: 'DELETE',
      headers: {
        'X-CSRFToken': getCookie('csrftoken') 
      }
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json(); 
    })
    .then(data => {
      alert(data.message);
      window.location.reload();
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error: ' + error.message);
    });
  }
  
  function toggleVisibility(itemId) {
    fetch(`/toggle-visibility/${itemId}/`, {
      method: 'PATCH', 
      headers: {
        'X-CSRFToken': getCookie('csrftoken'),
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({})
    })
    .then(response => response.json())
    .then(data => {
      alert(data.message);
      window.location.reload();
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error: ' + error.message);
    });
  }
  
  
  function getCookie(name) {
    let cookieValue = null;
    let cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
    }
    return cookieValue;
  }