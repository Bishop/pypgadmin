
function Connection(profile, action) {
	var c = {
		profile: profile,
		database: null,
		fetchDatabases: function() {

		},
		action: function(action) {
			if (['load', 'edit'].indexOf(action) != -1) {
				this[action](this.profile);
			}
		},
		load: function (profile) {
			$("#db_tree").load('/db/list/' + profile);
		},
		edit: function (profile) {

		}
	}
	c.action(action);
	return c;
}