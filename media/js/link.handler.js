function loadConnection(profile) {
	$("#db_tree").load('/db/' + profile);
}

(function ($) {
	$("#connections a").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var action = self.attr("rel");
		var profile = self.attr("href").substr(1)
		alert(profile + " " + action);
	})
})(jQuery);