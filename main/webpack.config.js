const path = require('path');
const webpack = require('webpack');

const LiveReloadPlugin = require('webpack-livereload-plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const ExtractTextPlugin = require('extract-text-webpack-plugin');
const CopyWebpackPlugin = require('copy-webpack-plugin');

const extractCss = (process.env.NODE_ENV === 'production')
	? new ExtractTextPlugin({ filename: '[contenthash].css' })
	: new ExtractTextPlugin({ filename: 'main.css' });

module.exports = {
	context: path.resolve(__dirname, 'src'),
	entry: './index.js',
	output:{
		path: __dirname + '/static',
		filename: 'main.js',
		publicPath: '/static/',
	},
	resolve:{
		modules:[
			path.resolve(__dirname, 'src/'),
			'node_modules',
		],
	},
	module:{
		rules:[
			{
				test: /\.js$/,
				use: ['babel-loader'],
				exclude: /node_modules/
			},
			{
				test: /\.css$/,
				use: extractCss.extract({
					fallback: 'style-loader',
					use: {
						loader: 'css-loader',
						options:{
							sourceMap:true,
							minimize:true,
						}
					},
				})
			},
			{
				test: /\.scss$/,
				use: extractCss.extract({
					fallback: 'style-loader',
					use: [
						{
							loader: 'css-loader',
							options:{
								minimize:true,
							}
						},
						{
							loader: 'sass-loader',
						}
					],
				})
			},
			{
				test: /\.less$/,
				use: extractCss.extract({
					fallback: 'style-loader',
					use: [
						{
							loader: 'css-loader',
							options:{
								minimize:true,
								sourceMap:true
							}
						},
						{
							loader: 'less-loader',
							options:{
								sourceMap: true,
								paths: [
									path.resolve(__dirname, 'src/assets'),
									path.resolve(__dirname, 'src/styles'),
									path.resolve(__dirname, 'node_modules'),
								]
							}
						}
					],
				}),
			},
			{
				test: /\.html$/, use: ['raw-loader']
			},
			{
				test: /\.(png|jpg|gif|svg|eot|otf|ttf|woff|woff2)$/,
				loader: 'url-loader',
				options: {
					limit: 10000
				}
			}
		],
	},
	watchOptions: {
		aggregateTimeout: 300,
		poll: 1000,
		ignored: /node_modules/
	},
	plugins: [
		new LiveReloadPlugin({}),
		extractCss,
		new HtmlWebpackPlugin({
			inject: false,
			title:'usias - request for proposal portal',
			filename: '../templates/base.html',
			template: './index.ejs',
			favicon: './favicon.ico'
		}),
		new CopyWebpackPlugin([
			// Copy directory contents to {output}/to/directory/
			{ from: './styles/fonts/', to: '../static/fonts/'},
			{ from: './styles/img/', to: '../static/img/'}
		], {})
	]
};
