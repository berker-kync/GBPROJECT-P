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

// Kaydet butonları için event listener ekleyin
document.querySelectorAll('.save-status').forEach(function(button) {
    button.addEventListener('click', function(event) {
        // Butonun data-order-id attributünden sipariş ID'sini alın
        var orderId = this.dataset.orderId;
        // Aynı sipariş ID'sine sahip durum seçiciyi bulun
        var selectElement = document.querySelector('.status-selector[data-order-id="' + orderId + '"]');
        // Seçilen durumu alın
        var status = selectElement.value;

        // AJAX isteğini PATCH metodu ile başlatın
        fetch('/update-order-status/' + orderId + '/', {
            method: 'PATCH', // RESTful API prensiplerine göre PATCH kullanılır
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken') // CSRF token'ı al
            },
            body: JSON.stringify({ status: status }) // Durum bilgisini JSON olarak gönderin
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json(); // JSON yanıtını döndür
        })
        .then(data => {
            if (data.status === 'success') {
                console.log('Durum güncellendi');
                // Burada başarı mesajı gösterebilirsiniz.
            } else {
                console.error('Bir hata oluştu: ' + data.message);
                // Burada hata mesajı gösterebilirsiniz.
            }
        })
        .catch(error => {
            console.error('Hata:', error);
            // Burada ağ hatası mesajı gösterebilirsiniz.
        });
    });
});

// CSRF token almak için yardımcı fonksiyon
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

