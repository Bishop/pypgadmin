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
		var p = self.parent("span");
		var child = p.next("div");
		if (child.children().size() == 0) {
			child.load(url + '/' + dbc.profile);
		} else {
			child.toggleClass('g-hidden');
		}
	});

	$("#db_tree a[rel=schema]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = self.attr("href").substr(1);
		var p = self.parent("span");
		var child = p.next("div");
		if (child.children().size() == 0) {
			url = p.parents("div.b-db:first").find("a[rel=db_name]:first").attr("href").substr(1) + '/' + url;
			child.load(url + '/' + dbc.profile);
		} else {
			child.toggleClass('g-hidden');
		}
	});

})(jQuery);