'use strict';

const path = require('path');
const webpack = require('webpack');
const merge = require("webpack-merge");
const HtmlWebPackPlugin = require("html-webpack-plugin");
const VueLoaderPlugin = require("vue-loader/lib/plugin");


/*const htmlPlugin = new HtmlWebPackPlugin({
    template: path.resolve(__dirname, './src/index.html'),
    filename: "./index.html"
});*/

//const APP_DIR = path.resolve(__dirname, './src');

module.exports = env => {
    return merge([
        {
            //context: path.join(__dirname, './src'),
            entry: ["./src/index.js"],
            output: {
                path: __dirname + '/dist',
                filename: "main.js",
                //publicPath: './'
                //path: path.resolve(__dirname, './dist')
            },
            module: {

                rules: [
                    {
                        test: [/\.js$/, /\.es6$/],
                        exclude: /node_modules/,
                        use: {
                            loader: "babel-loader",
                            options: {
                                "plugins":[
                                    "@babel/plugin-proposal-class-properties"
                                ]
                            }
                        }
                    },
                    /*{
                        test: /\.(jpe?g|png|gif|woff|woff2|eot|ttf|svg)(\?[a-z0-9=.]+)?$/,
                        use: [
                            {
                                loader: 'url-loader',
                                options: {
                                    limit: 100000
                                }
                            }
                        ]
                    },*/
                    {
                        test: /\.(png|svg|jpg|gif)$/,
                        use: [
                            {
                                loader: 'file-loader'
                            }
                        ]
                    },{
                        test: /\.vue$/,
                        use: [
                            {
                                loader: 'vue-loader',
                            }
                        ]
                    },{
                        test: /\.css$/,
                        use: [
                            'vue-style-loader',
                            'css-loader'
                            ]
                    },
                    /*,{
                        test: /\.(css|less)$/,
                        use: [{
                            loader: 'style-loader'
                        }, {
                            loader: "css-loader" // translates CSS into CommonJS
                        }, {
                            loader: "less-loader" // compiles Less to CSS
                        }
                        /!*, {
                            'vue-style-loader',
                            {
                                loader: 'css-loader',
                                options: {
                                    modules: true
                                }
                            }
*!/

                        ]
                    }*/
                ]
            },
            resolve: {

                extensions: ['*', '.js', '.jsx','.json','.vue'],
                alias: {
                    components:path.resolve(__dirname,'src/components'),
                    store:path.resolve(__dirname,'src/store'),
                    'vue$': 'vue/dist/vue.js'
                }
            },
            optimization: {
                splitChunks: {
                    chunks: 'all'
                }
            },
            plugins: [
                new VueLoaderPlugin(),
                new HtmlWebPackPlugin({
                    template: './src/index.html',
                    filename: "./index.html"
                }),
                new webpack.ProvidePlugin({
                    $: 'jquery',
                    jquery: 'jquery',
                    'window.jQuery': 'jquery',
                    jQuery: 'jquery'
                })

            ],

        }
    ])
};