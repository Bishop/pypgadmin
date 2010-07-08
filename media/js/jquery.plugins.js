
function Connection(profile, action) {
	var c = {
		profile: profile,
		database: null,
		fetchDatabases: function() {

		},
		action: function(action) {
			alert(action);
		}
	}
	c.action(action);
	return c;
}