function loadConnection(profile) {
	$("#db_tree").load('/db/' + profile);
}

var dbc;

(function ($) {
	$("#connections a").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var action = self.attr("rel");
		var profile = self.attr("href").substr(1);
		if (dbc == undefined || dbc.profile != profile) {
			dbc = new Connection(profile, action);
		} else {
			dbc.action(action);
		}
	})
})(jQuery);