/* RequireJS config */
require.config({
	shim: {
		'bootstrap': { 'deps': ['jquery'] },
	},
	paths: {
		'jquery': [
			'//code.jquery.com/jquery-2.2.3.min',
			'/static/content/jquery-2.2.3/jquery.min'
		],
		'bootstrap': [
			'//netdna.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min',
			'/static/content/bootstrap-3.3.6/js/bootstrap.min'
		],
		'moment': '/static/scripts/moment-with-locales',
	}
});