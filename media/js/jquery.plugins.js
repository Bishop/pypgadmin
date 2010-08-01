
function Connection(profile, action) {
	var c = {
		TPL_DB: '<div class="b-db">\
					<span class="b-db__dbname">\
						<a class="b-chevron" rel="db_name">Database</a>\
					</span>\
					<div class="b-schemas" />\
				</div>',
		profile: profile,
		currentTable: null,
		databases: null,
		fetchDatabases: function() {

		},
		action: function(action) {
			if (['load', 'edit'].indexOf(action) != -1) {
				this[action](this.profile);
			}
		},
		load: function (profile) {
			var area = $("#db_tree_" + profile);
			var self = this;
			jQuery.getJSON('/get_dbs/' + profile, function(data) {
				area.children().remove();
				this.databases = data;
				for (var i in data) {
					var db_name = data[i];
					var block = jQuery(self.TPL_DB);
					block.find("a[rel=db_name]").
							attr("href", "#db/" + db_name + "/" + self.profile).
							attr("title", db_name).
							text(db_name);
					block.appendTo(area);
				}

//				area.find("a[rel=db_name]").each(function(){
//					var self = $(this);
//					self.attr("href", self.attr("href") + "/" + profile);
//					if (self.parent("span").next("div").children().size() != 0) {
//						self.toggleClass("b-chevron__expand");
//					}
//				});
			});
		},
		edit: function (profile) {
			alert(profile);
		}
	};
	c.action(action);
	return c;
}