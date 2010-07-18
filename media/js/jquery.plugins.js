
function Connection(profile, action) {
	var c = {
		profile: profile,
		currentTable: null,
		database: null,
		fetchDatabases: function() {

		},
		action: function(action) {
			if (['load', 'edit'].indexOf(action) != -1) {
				this[action](this.profile);
			}
		},
		load: function (profile) {
			$("#db_tree").load('/server/' + profile, function(){
				$("#db_tree a[rel=db_name]").each(function(){
					if ($(this).parent("span").next("div").children().size() != 0) {
						$(this).toggleClass("b-chevron__expand");
					}
				});
			});
		},
		edit: function (profile) {
			alert(profile);
		}
	};
	c.action(action);
	return c;
}