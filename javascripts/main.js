$(document).ready(function () {
	var pathname = document.location.pathname;
	var last = pathname.lastIndexOf('/');
	var filename = pathname.substring(last + 1);

	$('#menu a[href="' + filename + '"]').parent().addClass('selected');
})
