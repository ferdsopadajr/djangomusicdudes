$(function() {
	$('.sidebar-nav li:not(:first-child) a').click(function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');
	})

	$('.song button').click(function() {
		console.log($(this).attr('id'));
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