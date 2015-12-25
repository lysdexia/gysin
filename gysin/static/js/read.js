$(document).ready(function () {
	var params = {
		size: "large",
		text: $("#poem-title").text() + " by " + $("#poem-author").text(),
		hashtags: "gysin"
	};

	twttr.widgets.createShareButton(
		window.location.href,
		document.getElementById("twit"),
		params
		).then(function (el) {
		console.log("how nice for you");
	});
});
