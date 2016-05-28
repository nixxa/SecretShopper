/* RequireJS config */
require.config({
	shim: {
		'bootstrap': { 'deps': ['jquery'] },
		'date-input': { 'deps': ['jquery'] }
	},
	paths: {
		'jquery': [
			'//code.jquery.com/jquery-2.2.3.min',
			'/static/content/jquery-2.2.3/jquery.min'
		],
		'bootstrap': [
			'//netdna.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap',
			'/static/content/bootstrap-3.3.6/js/bootstrap'
		],
		'moment': '/static/scripts/moment-with-locales',
		'date-input': '/static/content/datetime-input/js/date-input',
		'checklist.view': '/static/scripts/checklist.view'
	}
});