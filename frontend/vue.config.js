const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  transpileDependencies: true,
  
  devServer: {
    proxy: {
      '/api': {
        target: 'https://88bamboo.co',
        changeOrigin: true,
        pathRewrite: {
          '^/api': 'https://88bamboo.co'
        }
      }
    }
  },
  
  configureWebpack: {
    optimization: {
      splitChunks: {
        cacheGroups: {
          chartjs: {
            test: /[\\/]node_modules[\\/]chart\.js/,
            name: 'chartjs',
            chunks: 'all',
            priority: 20
          }
        }
      }
    }
  }
})