// gysin.js
$(document).ready(function() {
	// home button
	$("#home").click(function(){
		$(window).attr("location", "/");
	});

	// if we have a songspace element, fill it
	if ($("#songspace").length) {
		var line = "";
		$.get("api/chain", function(data) {
			$.each(data, function(idx, list){
				line = list.join(" ") + "\n";
				$("#songspace").append(line);
			});
		});
	}
});
