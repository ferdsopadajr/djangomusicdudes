var track_id;
$(function() {
	// sidebar link
	$('.sidebar-nav li:not(:first-child)').on('click', 'a', function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');
	});

	$.ajaxSetup({async: false});

	// display recommendations
	$('.main-view').on('click', '.fa-play', function() {
		track_id = $(this).parent().attr('id');
		$('.all-songs').removeClass('full');
		$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only').parent().siblings('.song').find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.player-controls-buttons .fa-play').addClass('sr-only').siblings('.fa-pause').removeClass('sr-only');
		$.post(
			'/upd_cbl/',
			{
				track_id: track_id
			},
			function(data) {
				console.log($('.song-info-name').val());
				$('.controls-bar-left').html(data);
				$('.controls-bar').attr('id',track_id);
			}
		);
		$.post(
			'/gen_rec/',
			{
				track_id: track_id
			},
			function(data) {
				$('.mood-rec').removeClass('sr-only').html(data);
			}
		);
	}).on('click', '.fa-pause', function() {
		$(this).addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.player-controls-buttons .fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
	});

	$('.main-view').on('click', '.fal.fa-heart', function() {
		track_id = $(this).parents('.song').attr('id');
		// add song to favorites
		$.post(
			'/add_to_fav/',
			{
				track_id: track_id
			}
		);
		$(this).addClass('sr-only').siblings('.fas.fa-heart').removeClass('sr-only');
		if ($('.controls-bar').attr('id') == track_id) {
			$('.controls-bar-left .fal.fa-heart').addClass('sr-only').siblings('.fas.fa-heart').removeClass('sr-only');
		}
	}).on('click', '.fas.fa-heart', function() {
		track_id = $(this).parents('.song').attr('id');
		// remove song to favorites
		$.post(
			'/del_to_fav/',
			{
				track_id: track_id
			}
		);
		$(this).addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
		if ($('.controls-bar').attr('id') == track_id) {
			$('.controls-bar-left .fas.fa-heart').addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
		}
	});

	$('.controls-bar-left').on('click', '.fal.fa-heart', function() {
		track_id = $(this).parents('.controls-bar').attr('id');
		// add song to favorites
		$.post(
			'/add_to_fav/',
			{
				track_id: track_id
			}
		);
		$(this).addClass('sr-only').siblings('.fas.fa-heart').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fal.fa-heart').addClass('sr-only').siblings('.fas.fa-heart').removeClass('sr-only');
	}).on('click', '.fas.fa-heart', function() {
		track_id = $(this).parents('.controls-bar').attr('id');
		// remove song to favorites
		$.post(
			'/del_to_fav/',
			{
				track_id: track_id
			}
		);
		$(this).addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fas.fa-heart').addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
	});

	// player controls
	$('.player-controls-buttons').on('click', '.fa-pause', function() {
		$(this).addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
	}).on('click', '.fa-play', function() {
		$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fa-play').addClass('sr-only').siblings('.fa-pause').removeClass('sr-only');
	}).on('click', '.fa-random, .fa-repeat-alt', function() {
		if ($(this).hasClass('but-clkd')) {
			$(this).removeClass('but-clkd');
			if ($(this).attr('title') == 'Disable shuffle') {
				$(this).attr('title','Enable shuffle');
			}
		} else {
			$(this).addClass('but-clkd');
			if ($(this).attr('title') == 'Enable repeat') {
				$(this).attr('title','Enable repeat one');
			} else if ($(this).attr('title') == 'Enable shuffle') {
				$(this).attr('title','Disable shuffle');
			}
		}
	}).on('click', '.fa-repeat-alt.but-clkd', function() {
		$(this).attr('title','Enable repeat');
		$(this).removeClass('but-clkd').addClass('sr-only').siblings('.fa-repeat-1-alt').removeClass('sr-only').addClass('but-clkd');
	}).on('click', '.fa-repeat-1-alt', function() {
		$(this).removeClass('but-clkd').addClass('sr-only').siblings('.fa-repeat-alt').removeClass('sr-only');
	});

	// display account settings
	$('.top-bar').on('click', '#account', function() {
		$.get(
			'/account/',
			function(data) {
				$('.main-view').html(data);
			}
		)
	});
});