// Setup AJAX to include CSRF token for Django
function getCookie(name) {
    let value = "; " + document.cookie;
    let parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

$.ajaxSetup({
    headers: { "X-CSRFToken": getCookie("csrftoken") }
});




(function ($) {

	"use strict";

	// Lazy load
	var lazyLoadInstance = new LazyLoad({
	    elements_selector: ".lazy"
	});

	// Header background
	$('.background-image').each(function(){
		$(this).css('background-image', $(this).attr('data-background'));
	});

	// Carousel categories home page
	var owlcat = $('.categories_carousel');
	owlcat.owlCarousel({
	    center: false,
	    stagePadding: 50,
	    items: 1,
	    loop: false,
	    margin: 20,
	    dots: false,
	    nav: true,
	    lazyLoad: true,
	    navText: ["<i class='arrow_left'></i>","<i class='arrow_right'></i>"],
	    responsive: {
	        0: {
	            nav: false,
	            dots: false,
	            items: 2
	        },
	        600: {
	            nav: false,
	            dots: false,
	            items: 2
	        },
	        768: {
	            nav: false,
	            dots: false,
	            items: 4
	        },
	        1025: {
	            nav: true,
	            dots: false,
	            items: 4
	        },
	        1340: {
	            nav: true,
	            dots: false,
	            items: 5
	        },
	        1460: {
	            nav: true,
	            dots: false,
	            items: 5
	        }
	    }
	});

	// Carousel home page
	var owl4 = $('.carousel_4');
		owl4.owlCarousel({
			items: 1,
			loop: false,
			stagePadding: 50,
			margin: 20,
			dots:false,
            lazyLoad:true,
			navText: ["<i class='arrow_left'></i>","<i class='arrow_right'></i>"],
			nav:false,
			responsive: {
			0: {
				items: 1
			},
			560: {
				items: 1
			},
			768: {
				items: 2
			},
			1230: {
				items: 3,
				nav: true
			}
		}
		});

	// Sticky nav
	$(window).on('scroll', function () {
		if ($(this).scrollTop() > 1) {
			$('.element_to_stick').addClass("sticky");
		} else {
			$('.element_to_stick').removeClass("sticky");
		}
	});
	$(window).scroll();
	
	// Menu
	$('a.open_close').on("click", function () {
		$('.main-menu').toggleClass('show');
		$('.layer').toggleClass('layer-is-visible');
	});
	$('a.show-submenu').on("click", function () {
		$(this).next().toggleClass("show_normal");
	});
	
	// Opacity mask
	$('.opacity-mask').each(function(){
		$(this).css('background-color', $(this).attr('data-opacity-mask'));
	});

	// Scroll to top
	var pxShow = 800; // height on which the button will show
	var scrollSpeed = 500; // how slow / fast you want the button to scroll to top.
	$(window).scroll(function(){
	 if($(window).scrollTop() >= pxShow){
		$("#toTop").addClass('visible');
	 } else {
		$("#toTop").removeClass('visible');
	 }
	});
	$('#toTop').on('click', function(){
	 $('html, body').animate({scrollTop:0}, scrollSpeed);
	 return false;
	});

	// Cart Dropdown Hidden From tablet
	$(window).bind('load resize', function () {
		var width = $(window).width();
		if (width <= 768) {
			$('a.cart_bt').removeAttr("data-bs-toggle", "dropdown")
		} else {
			$('a.cart_bt').attr("data-bs-toggle", "dropdown")
		}
	});
	
	// Footer collapse
	var $headingFooter = $('footer h3');
	$(window).resize(function() {
        if($(window).width() <= 768) {
      		$headingFooter.attr("data-bs-toggle","collapse");
        } else {
          $headingFooter.removeAttr("data-bs-toggle","collapse");
        }
    }).resize();
	$headingFooter.on("click", function () {
		$(this).toggleClass('opened');
	});

	// Scroll to position
    $('a[href^="#"].btn_scroll').on('click', function (e) {
			e.preventDefault();
			var target = this.hash;
			var $target = $(target);
			$('html, body').stop().animate({
				'scrollTop': $target.offset().top
			}, 800, 'swing', function () {
				window.location.hash = target;
			});
		});

	// Like Icon
    $('.btn_hero.wishlist').on('click', function(e){
    	e.preventDefault();
		$(this).toggleClass('liked');
	});

	// Modal Sign In
	$('#sign-in').magnificPopup({
		type: 'inline',
		fixedContentPos: true,
		fixedBgPos: true,
		overflowY: 'auto',
		closeBtnInside: true,
		preloader: false,
		midClick: true,
		removalDelay: 300,
		closeMarkup: '<button title="%title%" type="button" class="mfp-close"></button>',
		mainClass: 'my-mfp-zoom-in'
	});

	// Video modal
	$('.btn_play').magnificPopup({
		type: 'iframe',
		closeMarkup: '<button title="%title%" type="button" class="mfp-close" style="font-size:26px; margin-right:-10px;">&#215;</button>'
	});

// Modal
$(document).ready(function() {
    // Modal functionality
    $('.modal_dialog').magnificPopup({
        type: 'inline',
        fixedContentPos: true,
        fixedBgPos: true,
        overflowY: 'auto',
        closeBtnInside: true,
        preloader: false,
        midClick: true,
        removalDelay: 300,
        closeMarkup: '<button title="%title%" type="button" class="mfp-close"></button>',
        mainClass: 'my-mfp-zoom-in',
        callbacks: {
            beforeOpen: function() {
                // Get the clicked product ID
                let productId = this.st.el.attr('data-product-id');
                
                // Update the input field inside the modal with the clicked product ID
                $('#product_id').val(productId);
                
                // Set the form action based on the product ID
                this.content.find('form').attr('action', '/add_to_cart/' + productId);
            }
        }
    });

    // AJAX form submission
    $('form').on('submit', function(event) {
        event.preventDefault();  // Prevent the form from causing a page reload

        let formData = $(this).serialize();  // Serialize the form data

        $.ajax({
            type: $(this).attr('method'),  // Use the form's method (probably "post")
            url: $(this).attr('action'),   // Use the form's action
            data: formData,
            success: function(response) {
                // Handle the server's response here if needed
                // For now, we'll just log it to the console
                console.log(response);
            },
            error: function(error) {
                console.error("Error:", error);
            }
        });
    });
});


	

	// Modal images
	$('.magnific-gallery').each(function() {
	    $(this).magnificPopup({
	        delegate: 'a',
	        type: 'image',
	        preloader: true,
	        gallery: {
	            enabled: true
	        },
	        removalDelay: 500, //delay removal by X to allow out-animation
	        callbacks: {
	            beforeOpen: function() {
	                // just a hack that adds mfp-anim class to markup 
	                this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
	                this.st.mainClass = this.st.el.attr('data-effect');
	            }
	        },
	        closeOnContentClick: true,
	        midClick: true // allow opening popup on middle mouse click. Always set it to true if you don't provide alternative source.
	    });
	});

	// Show hide password login modal and register page
	$('#password, #password1, #password2').hidePassword('focus', {
		toggle: {
			className: 'my-toggle'
		}
	});

	// Forgot Password
	$("#forgot").on('click', function () {
		$("#forgot_pw").fadeToggle("fast");
	});

	// Jquery select
	$('.custom_select select').niceSelect();

	// Accordion
	function toggleChevron(e) {
		$(e.target)
			.prev('.card-header')
			.find("i.indicator")
			.toggleClass('icon_minus-06 icon_plus');
	}
	$('.accordion_2').on('hidden.bs.collapse shown.bs.collapse', toggleChevron);
		function toggleIcon(e) {
        $(e.target)
            .prev('.panel-heading')
            .find(".indicator")
            .toggleClass('icon_minus-06 icon_plus');
    }



	// Increment product quantity functionality

	$(document).on('click', '.increase-product-btn', function(e) {
		e.preventDefault();
		
		var productId = $(this).data('id');
		$.ajax({
			url: `/increase_quantity/${productId}/`,
			method: 'POST',
			data: {
				'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
			},
			success: function(response) {
				if(response.success) {
					alert('Success!');
					updateOrderSummary();
				} else {
					alert('Failed to update quantity.');
				}
			},
			error: function(error) {
				alert('Error occurred.');
			}
		});
	});
	
	function updateOrderSummary() {
		$.get('/products_in_basket/', function(data) {
			// Replace the order summary section with new content.
			$('#sidebar_fixed').html(data);
		});
	}
	









	// $(document).on('click', '.increase-product-btn', function(e) {
	// 	e.preventDefault();
		
	// 	var productId = $(this).data('id');
	// 	$.ajax({
	// 		url: `/increase_quantity/${productId}/`,
	// 		method: 'POST',
	// 		success: function(response) {
	// 			alert('Success!');
	// 		},
	// 		error: function(error) {
	// 			alert('Error occurred.');
	// 		}
	// 	});
	// });


})(window.jQuery); 