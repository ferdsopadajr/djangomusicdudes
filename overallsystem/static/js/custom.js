var track_id;
var track_max_duration;
var listening_duration;
var counter;
var past_track;

// timer
function countdown() {
	console.log(listening_duration);
	if (listening_duration <= 0) {
		clearInterval(counter);
		console.log('ldend: '+listening_duration);
		return;
	}
	listening_duration -= 1000;
	width = 100 - ((listening_duration / track_max_duration) * 100);
	console.log(width);
	document.getElementById('playback-bar').style.width = width+'%';
	document.getElementById('playback-bar').setAttribute('aria-valuenow', track_max_duration - listening_duration);
	console.log(listening_duration);
}

$(function() {
	// sidebar link
	$('.sidebar-nav li:not(:first-child)').on('click', 'a', function() {
		$(this).parent().addClass('active').siblings().removeClass('active').find('i').css('color','');
		$(this).find('i').css('color','#2b5b84');

		if ($(this).attr('id') == '#favorites') {
			// display favorites
			$.post(
				'/favorites/',
				function(data) {
					$('.all-songs').html(data);
				}
			);
		} else if ($(this).attr('id') == '#browse') {
			$.post(
				'/main/',
				function(data) {
					$('body').html(data);
				}
			);
		}
	});

	$.ajaxSetup({async: false});

	// display recommendations
	$('.main-view').on('click', '.fa-play', function() {
		track_id = $(this).parent().attr('id');
		clearInterval(counter);
		track = null;
		if ($('.controls-bar').attr('id')) {
			past_track = $('.controls-bar').attr('id');
		}
		console.log(past_track);
		$('.all-songs').removeClass('full');
		$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only').parent().siblings('.song').find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$.post(
			'/upd_cbl/',
			{
				track_id: track_id
			},
			function(data) {
				console.log($('.song-info-name').val());
				$('.controls-bar-left-center').html(data);
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
				$('.player-controls-buttons .fa-play').addClass('sr-only').siblings('.fa-pause').removeClass('sr-only');
			}
		);
		$.post(
			'/duration/',
			{
				track_id: track_id
			},
			function(data) {
				track_max_duration = data;
				listening_duration = track_max_duration;
				console.log(track_max_duration);
			}
		);
		counter = setInterval(countdown, 1000);
		$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only').parent().siblings('.song').find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
	}).on('click', '.fa-pause', function() {
		clearInterval(counter);
		console.log(listening_duration);
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

	$('.controls-bar-left-center').on('click', '.fal.fa-heart', function() {
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
	$('.controls-bar-left-center').on('click', '.fa-pause', function() {
		clearInterval(counter);
		console.log(listening_duration);
		$(this).addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
	}).on('click', '.fa-play', function() {
		counter = setInterval(countdown, 1000);
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
		$.post(
			'/account/',
			function(data) {
				$('.main-view').html(data);
			}
		);
	});
});