$(function() {
	$('.sidebar-nav li:not(:first-child) a').click(function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');
	})
});