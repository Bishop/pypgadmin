var dbc = new Array();

(function ($) {
	function select_table_tab() {
		$("#table_view_menu a[href=#structure]").toggleClass('m-tab__selected', document.getElementById("table_structure") != undefined);
		$("#table_view_menu a[href=#data]").toggleClass('m-tab__selected', document.getElementById("table_data") != undefined);
	}

	$(".tableLink").live('click', function(event){
		event.preventDefault();
		var url = 'db/' + $(this).attr("href");
		$("#content").load(url + '/' + app.getConnectionByElement(this), function() {
			select_table_tab();
			dbc.currentTable = url;
		});
	})

	$("#table_view_menu a[rel=current_table]").live('click', function(event){
		event.preventDefault();
		var self = $(this);
		var url = dbc.currentTable + '/' + self.attr("href").substr(1) + '/' + app.getConnectionByElement(this);
		$("#content").load(url, function() {
			select_table_tab();
		});
	});

})(jQuery);