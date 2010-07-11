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
	});

	$("#server_menu a").live('click', function(event){
		var url = $(this).attr("href").substr(1);
		$("#content").load(url);
	});

	$("#db_tree a[rel=db_name]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = self.attr("href").substr(1);
		self.parent("span").next("div.b-schemas").load(url + '/' + dbc.profile);
	});

})(jQuery);