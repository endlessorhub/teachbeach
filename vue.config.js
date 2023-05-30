const path = require('path')
const _ = require('lodash')
const webpack = require('webpack')
const webpackConf = require('./webpack.config')
const outputDir = webpackConf.output.path
const publicPath = webpackConf.output.publicPath
delete webpackConf.output.path
delete webpackConf.output.publicPath
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const CopyWebpackPlugin = require('copy-webpack-plugin')
const PreloadWebpackPlugin = require('preload-webpack-plugin')
const CompressionPlugin = require('compression-webpack-plugin')
const routesToSitemap = require('./js/src/routes_to_sitemap')
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin;
const DotenvPlugin = require('webpack-dotenv-plugin');

const JS_FOLDER = path.join(__dirname, 'js/')
const STATIC_FOLDER = path.join(__dirname, 'teachbeach/static/')
const DJANGO_TEMPLATES_FOLDER = path.join(__dirname, 'teachbeach/templates/')

webpackConf.plugins = [
    new VuetifyLoaderPlugin(),
    new HtmlWebpackPlugin(
      {
        filename: path.join(DJANGO_TEMPLATES_FOLDER, '_app.html'),
        template: path.join(DJANGO_TEMPLATES_FOLDER, 'app.html')
      }
    ),
    new DotenvPlugin({
      path: './.env',
      sample: './.env',
    }),
    new webpack.DefinePlugin({
      'process.env': JSON.stringify(process.env),
    }),
    new PreloadWebpackPlugin({
        rel: 'preload',
        as: 'font',
        include: 'allAssets',
        fileWhitelist: [/\.(woff2?|eot|ttf|otf)(\?.*)?$/i],
        fileBlacklist: [/MaterialIcons.*\.(woff2?|eot|ttf|otf)(\?.*)?$/i],
    }),
    new webpack.ContextReplacementPlugin(/moment[\/\\]locale$/, /(en|us)$/),
    new CopyWebpackPlugin([
        {
            from: path.join(JS_FOLDER, '/src/routes.js'),
            to: path.join(JS_FOLDER, '/src/sitemap_template.json'),
            transform(content, absoluteFrom) {
                return routesToSitemap(content);
            },
        }
    ]),
    new CompressionPlugin(),
    //new BundleAnalyzerPlugin(),
]

webpackConf.entry = {
   app: './js/src/main.js'
 }

module.exports = {
  outputDir:outputDir,
  publicPath: publicPath,
  configureWebpack: _.pick(webpackConf, ['mode', 'devtool', 'output', 'resolve', 'resolveLoader', 'entry', 'plugins'])
}