
function Connection(profile, action) {
	var c = {
		TPL_DB: '<div class="b-db">\
					<span class="b-db__dbname">\
						<a class="b-chevron" rel="db_name">Database</a>\
					</span>\
					<div class="b-schemas" />\
				</div>',
		TPL_SCHEMA: '<div class="b-schema">\
						<span class="b-schema__name">\
							<a class="b-chevron" rel="schema">Schema</a>\
						</span>\
						<div class="b-tables" />\
					</div>',
		profile: profile,
		currentTable: null,
		databases: new Array(),
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
				for (var i in data) {
					var db_name = data[i];
					self.databases[db_name] = new Array();
					
					var block = jQuery(self.TPL_DB);
					block.find("a[rel=db_name]").
							attr("href", "#db/" + db_name).
							attr("title", db_name).
							text(db_name).
							click(function(event){
								event.preventDefault();
								self.load_schemas(jQuery(this), db_name);
					});
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
		is_empty: function(block) {
			if (block.children().size() == 0) {
				return true;
			} else {
				block.toggleClass('g-hidden');
				return false;
			}
		},
		load_schemas: function(link, db_name) {
			var url = "get_schemas/" + link.attr("href").substr(4) + "/" + this.profile;
			var area = link.parent("span").next("div");
			if (this.is_empty(area)) {
				var self = this;
				jQuery.getJSON(url, function(data) {
					area.children().remove();
					for (var i in data) {
						var schema = data[i];
						//self.databases

						var block = jQuery(self.TPL_SCHEMA);
						block.find("a[rel=schema]").
								attr("href", "#schema/" + schema).
								attr("title", schema).
								text(schema);//.
//								click(function(event){
//									event.preventDefault();
//									self.load_schemas(jQuery(this), db_name);
						//})
						block.appendTo(area);
					}
				});
			}
		},
		edit: function (profile) {
			alert(profile);
		}
	};
	c.action(action);
	return c;
}