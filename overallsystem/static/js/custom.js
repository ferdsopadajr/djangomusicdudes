$(function() {
	$('.sidebar-nav li:not(:first-child) a').click(function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');
	})

	$('.song').click(function() {
		$.post(
			'/gen_rec/',
			{
				track_id: $(this).attr('id')
			},
			function(data) {
				$('.rec-container').html(data);
			}
		);
	})
});