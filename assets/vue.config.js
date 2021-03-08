module.exports = {
  devServer: {
    proxy: {
      "^/api": {
        // TODO: From configuration.
        target: "http://localhost:5000",
        changeOrigin: true
        // logLevel: 'debug'
      }
    }
  }
};
