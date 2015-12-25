// gysin.js

// fill chainspace with lines of artfully arranged text
function fillChainSpace () {
	var chainverse = [];
	var line = $("#chainspace").val();

	if (line) {
		chainverse.push(line);
	}

	$("#chainwrap").hide();
	$("#spinnerspace").show();
	$.get("api/chain", function(data) {
		$.each(data, function(idx, list){
			line = list.join(" ");
			chainverse.push(line);
		});
		$("#chainspace").val(chainverse.join("\n"));
		$("#chainwrap").show();
		$("#spinnerspace").hide();
	});
};

// append text selected/edited in chainspace to text in songspace
function appendSongSpace () {
	var verse = [];
	var line = $("#songspace").val();
	if (line) {
		verse.push(line + "  ");
	}
	verse.push($("#chainspace").val());
	$("#songspace").val(verse.join("\n"));
};

// join string with double spaces to make soft returns for markdown
function saveSongSpace () {
	var song = $("#songspace").val();
	song = song.split("\n");
	$("#songspace").val("\n" + song.join("  "));
};

$(document).ready(function() {
	$("#poesy").hide();
	$("#instructions").hide();

	// use html5 form validation 
	// there is some trickery in "save" below, since we don't actually
	// submit the form.
	$("#songspace").prop("required", true);
	$("#poem_title").prop("required", true);
	$("#author").prop("required", true);

	// if we have a chainspace element, fill it
	if ($("#chainspace").length) {
		if ($("chainspace").val() === undefined) {
			fillChainSpace();
		}
	}

	// home button listener
	$("#home").click(function() {
		$(window).attr("location", "/");
	});

	// more button appends more words to the chainspace element
	$("#more").click(function() {
		fillChainSpace();
		return false;
	});

	// save button tacks chainspace text onto songspace text prior to publishing
	$("#save").click(function() {
		$("#bound").hide();
		$("#poesy").show();
		appendSongSpace();
		return false;
	});

	// clear chainspace
	$("#chainspace-clear").click(function() {
		$("#chainspace").val("");
		return false;
	});	

	// save songspace
	// included bletcherous hack to enable html5 form validation without
	// actually submitting the form.
  	// hidden submit input is .click()ed programatically when #save gets
	// click event. I know, I suck.
	// Also: for some reason jquery throws an error (at least in this case)
	// when one actually uses the id of the form we are using checkValdidity()
	// on. Using the numeric value of the form works without throwing an error.
	$("#publish").click(function() {
		// kick off html5 validation
		if (!$("form")[0].checkValidity()) {
			$("#noshow").click();
			return false;
		}
		saveSongSpace();
		$("#noshow").click();
	});	

	// start the spinner a spinnin'
	var opts = {
		lines: 13 // The number of lines to draw
		, length: 4 // The length of each line
		, width: 5 // The line thickness
		, radius: 21 // The radius of the inner circle
		, scale: 1 // Scales overall size of the spinner
		, corners: 0.4 // Corner roundness (0..1)
		, color: '#000' // #rgb or #rrggbb or array of colors
		, opacity: 0.2 // Opacity of the lines
		, rotate: 0 // The rotation offset
		, direction: -1 // 1: clockwise, -1: counterclockwise
		, speed: 1.5 // Rounds per second
		, trail: 55 // Afterglow percentage
		// Frames per second when using setTimeout()
		//as a fallback for CSS
		, fps: 20 
		, zIndex: 2e9 // The z-index (defaults to 2000000000)
		, className: 'spinner' // The CSS class to assign to the spinner
		, top: '35%' // Top position relative to parent
		, left: '35%' // Left position relative to parent
		, shadow: true // Whether to render a shadow
		, hwaccel: true // Whether to use hardware acceleration
		, position: 'relative' // Element positioning
	}
	var target = document.getElementById("spinnerspace");
	var spinner = new Spinner(opts).spin(target);

	$("#show-instructions").click(function() {
		$("#instructions").fadeIn();
	});

	$("#got-it").click(function() {
		$("#instructions").fadeOut();
	});
});
