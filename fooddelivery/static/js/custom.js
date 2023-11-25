// window.addEventListener('load', function() {
//     const messages = document.querySelectorAll('.messages li');
//     messages.forEach(function(msg) {
//         setTimeout(function() { 
//             msg.style.display = 'none'; 
//         }, 3000); // 3000 milisaniye sonra mesajı gizle
//     });
// });
window.addEventListener('load', function() {
    const messages = document.querySelectorAll('.messages li');
    messages.forEach(function(msg) {
        setTimeout(function() { 
            msg.remove(); // Mesajı DOM'dan tamamen kaldır
        }, 3000); // 3000 milisaniye sonra mesajı kaldır
    });
});
