var dbc = new Array();

(function ($) {
	function select_table_tab() {
		$("#table_view_menu a[href=#structure]").toggleClass('m-tab__selected', document.getElementById("table_structure") != undefined);
		$("#table_view_menu a[href=#data]").toggleClass('m-tab__selected', document.getElementById("table_data") != undefined);
	}
	$("#connections a").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var action = self.attr("rel");
		var profile = self.attr("href").substr(1);
		if (dbc[profile] == undefined) {
			dbc[profile] = new Connection(profile, action);
		} else {
			dbc[profile].action(action);
		}
	});

	$("#server_menu a").live('click', function(event){
		var url = $(this).attr("href").substr(1);
		$("#content").load(url);
	});

	$(".db_tree a[rel=schema]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = self.attr("href").substr(1);
		var p = self.parent("span");
		var child = p.next("div");
		if (child.children().size() == 0) {
			url = p.parents("div.b-db:first").find("a[rel=db_name]:first").attr("href").substr(1) + '/' + url;
			child.load(url);
		} else {
			child.toggleClass('g-hidden');
		}
	});

	$(".db_tree a.b-chevron").live('click', function(event) {
		$(this).toggleClass("b-chevron__expand");
	});

	$(".db_tree a[rel=table]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = self.attr("href").substr(1);
		url = self.parents("div.b-db:first").find("a[rel=db_name]:first").attr("href").substr(1) + '/' +
			self.parents("div.b-schema:first").find("a[rel=schema]:first").attr("href").substr(1) + '/' + url;
		$("#content").load(url, function() {
			select_table_tab();
			dbc.currentTable = url;
		});
	})

	$("#table_view_menu a[rel=current_table]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = dbc.currentTable + '/' + self.attr("href").substr(1);
		$("#content").load(url, function() {
			select_table_tab();
		});
	});

})(jQuery);