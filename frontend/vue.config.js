const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})
module.exports = {
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
  }
}
