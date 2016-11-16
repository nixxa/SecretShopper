/* RequireJS config */
require.config({
	urlArgs: 'r=v1',
	shim: {
		'bootstrap': { 'deps': ['jquery'] },
		'date-input': { 'deps': ['jquery'] },
		'dropzone': { 'deps' : ['jquery'] },
		'datatables': { 'deps': ['jquery'] }
	},
	paths: {
		'jquery': [
			'https://code.jquery.com/jquery-2.2.3.min',
			'/static/content/jquery-2.2.3/jquery.min'
		],
		'bootstrap': [
			'https://netdna.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap',
			'/static/content/bootstrap-3.3.6/js/bootstrap'
		],
		'moment': '/static/content/momentjs/moment-with-locales',
		'date-input': '/static/content/datetime-input/js/date-input',
		'dropzone': '/static/content/dropzonejs/dropzone',
		'audiojs': '/static/content/audiojs/audio.min',
		'datatables': '/static/content/datatables/datatables',
		'pica': '/static/content/pica/pica.min'
	}
});