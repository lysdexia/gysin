var updateStatusCallback = function (response) {
	if (response.status === "connected") {
		var uid = response.authResponse.userID;
		var accessToken = response.authResponse.accessToken;
		console.log("they're heeeeere");
	} else if (response.status === "not_authorized") {
		console.log("not authorized");
	} else {
		console.log("not logged on");
	}
};

$(document).ready(function() {
	$.ajaxSetup({ cache: true });
	$.getScript('//connect.facebook.net/en_US/sdk.js', function(){
		FB.init({
			appId: '1446864582299246',
			version: 'v2.3'
		});
		//$('#loginbutton, #feedbutton').removeAttr('disabled');
		//FB.getLoginStatus(updateStatusCallback);
		FB.ui({
			method: "share",
			href: "//developers.facebook.com/docs/"
		}, function(response){
			console.log(response);
		});
	});
});


/*
window.fbAsyncInit = function() {
	FB.init({
		appId: '1446864582299246',
		xfbml: true,
		version: 'v2.3'
	});
};
(function(d, s, id){
	var js, fjs = d.getElementsByTagName(s)[0];
	if (d.getElementById(id)) {
		return;
	}
	js = d.createElement(s); js.id = id;
	js.src = "//connect.facebook.net/en_US/sdk.js";
	fjs.parentNode.insertBefore(js, fjs);
}(document, 'script', 'facebook-jssdk'));
*/
