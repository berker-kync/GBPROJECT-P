// // Tüm durum seçicileri için event listener ekleyin
// document.querySelectorAll('.status-selector').forEach(function(selector) {
//     selector.addEventListener('change', function(event) {
//         var orderId = this.dataset.orderId; // data-order-id özelliğinden sipariş ID'sini alın
//         var status = this.value; // Seçilen yeni durumu alın

//         // AJAX isteğini PATCH metodu ile başlatın
//         fetch('/update-order-status/' + orderId + '/', {
//             method: 'PATCH', // RESTful API prensiplerine göre PATCH kullanılır
//             headers: {
//                 'Content-Type': 'application/json',
//                 'X-CSRFToken': getCookie('csrftoken') // CSRF token'ı Django'dan al
//             },
//             body: JSON.stringify({ status: status }) // Durum bilgisini JSON olarak gönderin
//         })
//         .then(response => {
//             if (!response.ok) {
//                 throw new Error('Network response was not ok');
//             }
//             return response.json(); // JSON yanıtını döndür
//         })
//         .then(data => {
//             if (data.status === 'success') {
//                 console.log('Durum güncellendi');
//             } else {
//                 console.error('Bir hata oluştu: ' + data.message);
//             }
//         })
//         .catch(error => console.error('Hata:', error)); // Hata yönetimi
//     });
// });

// // CSRF token almak için yardımcı fonksiyon
// function getCookie(name) {
//     let cookieValue = null;
//     if (document.cookie && document.cookie !== '') {
//         const cookies = document.cookie.split(';');
//         for (let i = 0; i < cookies.length; i++) {
//             const cookie = cookies[i].trim();
//             if (cookie.substring(0, name.length + 1) === (name + '=')) {
//                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
//                 break;
//             }
//         }
//     }
//     return cookieValue;
// }


document.querySelectorAll('.save-status').forEach(function (button) {
    button.addEventListener('click', function (event) {
   
        var orderId = this.dataset.orderId;
        console.log('Clicked on save button for order:', orderId);

   
        var selectElement = document.querySelector('.status-selector[data-order-id="' + orderId + '"]');

        var status = selectElement.value;
        console.log('Selected status:', status);


        fetch('/update-order-status/' + orderId + '/', {
            method: 'PATCH', 
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') 
            },
            body: JSON.stringify({ status: status })
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); 
            })
            .then(data => {
                if (data.status === 'success') {
                    console.log('Durum güncellendi');
                    location.reload();
                } else {
                    console.error('Bir hata oluştu: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Hata:', error);
            });
    });
});


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener('DOMContentLoaded', function () {
    const statusSelectors = document.querySelectorAll('.status-selector');

    statusSelectors.forEach(selector => {
        selector.addEventListener('change', function () {
            const orderId = this.dataset.orderId;
            const selectedStatus = this.value;
            console.log(`Order ${orderId} status changed to ${selectedStatus}`);

            const orderRow = document.querySelector(`tr[data-order-id="${orderId}"]`);
            console.log('Order row:', orderRow);

            const statusSection = document.querySelector(`#${selectedStatus.toLowerCase()}-section .status-table`);
            console.log('Status section:', statusSection);
            statusSection.appendChild(orderRow);
        });
    });
});


