$(document).ready(function(){
	//  Menu and icon changing  
	$('.hamburger').on('click', function(e)
	{
		e.preventDefault();
		$(this).toggleClass('opned');
		$('header nav').toggleClass('active');
	});
});