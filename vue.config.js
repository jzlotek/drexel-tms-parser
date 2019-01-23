const CompressionPlugin = require('compression-webpack-plugin');
const zopfli = require('@gfx/zopfli');
const VuetifyLoaderPlugin = require('vuetify-loader/lib/plugin');

module.exports = {
  runtimeCompiler: true,
  publicPath: '',
  outputDir: './dist',
  assetsDir: 'static',
  productionSourceMap: false,
  parallel: true,
  css: {
    extract: true,
  },

  pwa: {
    name: 'drexel-tms',
    themeColor: '#040BC0',
    msTileColor: '#040BC0',
  },
  configureWebpack: {
    optimization: {
      minimize: true,
    },
    plugins: process.env.NODE_ENV === 'production' ? [
      new VuetifyLoaderPlugin(),
      new CompressionPlugin({
        filename: '[path].gz[query]',
        compressionOptions: {
          numiterations: 15,
        },
        algorithm(input, compressionOptions, callback) {
          return zopfli.gzip(input, compressionOptions, callback);
        },
      }),
    ] : [],
  },
};
