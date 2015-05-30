// gysin.js

// fill chainspace with lines of artfully arranged text
function fillChainSpace () {
	var chainverse = [];
	var line = $("#chainspace").val();

	if (line) {
		chainverse.push(line);
	}

	$.get("api/chain", function(data) {
		$.each(data, function(idx, list){
			line = list.join(" ");
			chainverse.push(line);
		});
		$("#chainspace").val(chainverse.join("\n"));
	});
};

// append text selected/edited in chainspace to text in songspace
function appendSongSpace () {
	var verse = [];
	var line = $("#songspace").val();
	if (line) {
		console.log("found line");
		verse.push(line);
	}
	console.log(verse);
	verse.push($("#chainspace").val());
	console.log(verse);
	$("#songspace").val(verse.join("\n"));
};


$(document).ready(function() {

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

	// append button tacks chainspace text onto songspace text
	$("#append").click(function() {
		appendSongSpace();
		return false;
	});

	// clear chainspace
	$("#chainspace-clear").click(function() {
		$("#chainspace").val("");
		return false;
	});	

	// clear songspace
	$("#songspace-clear").click(function() {
		$("#songspace").val("");
		return false;
	});	

	// save songspace
	$("#save").click(function() {
		alert("Totally alpha, man.");
		return false;
	});	

});
