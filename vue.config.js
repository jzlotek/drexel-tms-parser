module.exports = {
  runtimeCompiler: true,
  publicPath: '',
  outputDir: './dist',
  assetsDir: 'static',
  productionSourceMap: false,
  parallel: true,
  css: {
    extract: false
  },

  pwa: {
    name: 'drexel-tms',
    themeColor: '#040BC0',
    msTileColor: '#040BC0'
  }
}