$(document).ready(() => {
	// Show / Hide menu when clicked
	$('.has-sub').on('click', function(e) { 
		$('.dropdown-menu').not($(this).children('.dropdown-menu')).removeClass('dropdown-shown'); // Hide other menus
		$('.has-sub').not($(this)).removeClass('active');
		$(this).children('.dropdown-menu').toggleClass('dropdown-shown');
		$(this).toggleClass('active');
	});

	// TOGGLE HEADER-NAV
	$('#header-btn').on('click', function(e) {
		$('#header-menu').toggleClass('active');
		$('.nav-btn').toggleClass('active');
	});

	// Remove parent upon clicking close button
	$('.btn-close').on('click', function() {
		$(this).closest('div').remove();
	});
});
