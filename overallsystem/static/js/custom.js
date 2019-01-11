$(function() {
	$('.sidebar-nav li:not(:first-child)').on('click', 'a', function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');
	});

	$('.main-view').on('click', '.song', function() {
		$.post(
			'/gen_rec/',
			{
				track_id: $(this).attr('id')
			},
			function(data) {
				$('.rec-container').html(data);
			}
		);
	});

	$('.top-bar').on('click', '#account', function() {
		$.get(
			'/account/',
			function(data) {
				$('.main-view').html(data);
			}
		)
	});
});