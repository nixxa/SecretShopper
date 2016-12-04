var ExtractTextPlugin = require("extract-text-webpack-plugin");

module.exports = {
    entry: {
        bundle: "./src/js/bundle.js"
    },
    output: {
        path: 'frontui/static/assets/',
        publicPath: '/static/assets/',
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
                loader: 'file-loader?name=fonts/[name].[ext]' 
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