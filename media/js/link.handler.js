var dbc = new Array();

(function ($) {
	function select_table_tab() {
		$("#table_view_menu a[href=#structure]").toggleClass('m-tab__selected', document.getElementById("table_structure") != undefined);
		$("#table_view_menu a[href=#data]").toggleClass('m-tab__selected', document.getElementById("table_data") != undefined);
	}
	$("#connectionList a").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var action = self.attr("rel");
		var profile = self.find('.link').text();

		if (dbc[profile] == undefined) {
			dbc[profile] = new Connection(profile, action);
		} else {
			dbc[profile].action(action);
		}
	});

	$(".db_tree a[rel=table]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = self.attr("href").substr(1);
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