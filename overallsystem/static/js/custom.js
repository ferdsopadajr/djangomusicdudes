var track_id;
var track_max_duration;
var listening_duration;
var counter;
var past_track;
var fav_max;

$(function() {
	// timer
	function countdown() {
		var reducer = 1000;
		if (listening_duration < 1000 && listening_duration > 0) {
			reducer = listening_duration;
		}
		listening_duration -= reducer;
		width = 100 - ((listening_duration / track_max_duration) * 100);
		document.getElementById('playback-bar').style.width = width+'%';
		document.getElementById('playback-bar').setAttribute('aria-valuenow', track_max_duration - listening_duration);
		if (listening_duration <= 0) {
			clearInterval(counter);
			return;
		}
		$.post(
			'/convert_time/',
			{
				play_duration: track_max_duration-listening_duration
			},
			function(data) {
				$('#play-duration').text(data);
			}
		);
	}
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
				'/browse/',
				function(data) {
					$('.songs-container').html(data);
				}
			);
		}
	});

	$.ajaxSetup({async: false});

	// display recommendations
	$('.main-view').on('click', '.fa-play', function() {
		track_id = $(this).parent().attr('id');
		if ($('.controls-bar').attr('id')) {
			past_track = $('.controls-bar').attr('id');
		}
		if (past_track != track_id) {
			clearInterval(counter);
			$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only').parent().siblings('.song').find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
			$.post(
				'/upd_cbl/',
				{
					track_id: track_id
				},
				function(data) {
					$('.controls-bar-left-center').html(data);
					$('.controls-bar').attr('id',track_id);
					$('.player-controls-buttons button').removeAttr('disabled');
				}
			);
			if (past_track != null) {
				$.post(
					'/add_to_pref/',
					{
						past_track: past_track,
						play_duration: track_max_duration-listening_duration,
						max_duration: track_max_duration
					},
					function(data) {
						$('#'+past_track+' .ratings').text(data);
					}
				);
				if ((track_max_duration-listening_duration) >= (track_max_duration/2)) {
					$.post(
						'/gen_rec/',
						{
							track_id: track_id
						},
						function(data) {
							$('.all-songs').removeClass('full');
							$('.mood-rec').removeClass('sr-only').html(data);
						}
					);
				}
			}
			$.post(
				'/duration/',
				{
					track_id: track_id
				},
				function(data) {
					listening_duration = track_max_duration = data;
				}
			);
			$.post(
				'/backend_process/',
				{
					track_id: track_id
				}
			);
		}
		counter = setInterval(countdown, 1000);
		$(this).addClass('sr-only').siblings('.fa-pause').removeClass('sr-only').parent().siblings('.song').find('.fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.player-controls-buttons .fa-play').addClass('sr-only').siblings('.fa-pause').removeClass('sr-only');
	}).on('click', '.fa-pause', function() {
		clearInterval(counter);
		$(this).addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
		$('.player-controls-buttons .fa-pause').addClass('sr-only').siblings('.fa-play').removeClass('sr-only');
	});

	$('.main-view').on('click', '.fal.fa-heart', function() {
		track_id = $(this).parents('.song').attr('id');
		// add song to favorites
		$.post(
			'/duration/',
			{
				track_id: track_id
			},
			function(data) {
				fav_max = data;
			}
		);
		$.post(
			'/add_to_fav/',
			{
				track_id: track_id,
				max_duration: fav_max
			}
		);
		$.post(
			'/gen_rec/',
			{
				track_id: track_id
			},
			function(data) {
				$('.all-songs').removeClass('full');
				$('.mood-rec').removeClass('sr-only').html(data);
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
			},
			function(data) {
				if (data == 'False') {
					$('.all-songs').addClass('full');
					$('.mood-rec').addClass('sr-only');
				}
			}
		);
		$.post(
			'/gen_rec/',
			{
				track_id: track_id
			},
			function(data) {
				// $('.all-songs').removeClass('full');
				// $('.mood-rec').removeClass('sr-only').html(data);
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
			'/duration/',
			{
				track_id: track_id
			},
			function(data) {
				fav_max = data;
			}
		);
		$.post(
			'/add_to_fav/',
			{
				track_id: track_id,
				max_duration: fav_max
			}
		);
		$.post(
			'/gen_rec/',
			{
				track_id: track_id
			},
			function(data) {
				$('.all-songs').removeClass('full');
				$('.mood-rec').removeClass('sr-only').html(data);
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
			},
			function(data) {
				if (data == 'False') {
					$('.all-songs').addClass('full');
					$('.mood-rec').addClass('sr-only');
				}
			}
		);
		$.post(
			'/gen_rec/',
			{
				track_id: track_id
			},
			function(data) {
				// $('.all-songs').removeClass('full');
				// $('.mood-rec').removeClass('sr-only').html(data);
			}
		);
		$(this).addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
		$('.main-view').find('div#'+track_id).find('.fas.fa-heart').addClass('sr-only').siblings('.fal.fa-heart').removeClass('sr-only');
	});

	// player controls
	$('.controls-bar-left-center').on('click', '.fa-pause', function() {
		clearInterval(counter);
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