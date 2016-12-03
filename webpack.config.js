var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        index: "./src/js/index.js",
        checklist: "./src/js/checklist.view.js",
        'checklist.addfiles': './src/js/checklist.addfiles.view.js',
        reports: "./src/js/reports.view.js",
        'reports.object': "./src/js/reports.object.view.js"
    },
    output: {
        path: 'frontui/static/assets/',
        filename: "[name].js",
        chunkFilename: "[id].js"
    },
    module: {
        loaders: [
            {
                test: /\.js$|\.jsx$/,
                loader: "babel-loader",
                exclude: /node_modules/,
                query: {
                    plugins: ['transform-runtime'],
                    presets: ['es2015', 'stage-1']
                }
            },
            { 
                test: /\.css|\.less$/, 
                loader: ExtractTextPlugin.extract("css!less")
            },
            // Font Definitions
            { 
                test: /\.(ttf|eot|svg|woff(2)?)(\?[a-z0-9=&.]+)?$/, 
                loader: 'url-loader' 
            },
        ]
    },
    plugins: [
        new ExtractTextPlugin("css/[name].css")
    ],
    node: {
        fs: "empty"
    }
};