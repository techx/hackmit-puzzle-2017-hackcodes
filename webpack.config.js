var path = require('path')

module.exports = {
  entry: [
    './js/app.js'
  ],
  output: {
    path: path.join(__dirname, '/static'),
    filename: 'bundle.js'
  },
  module: {
    loaders: [
      {
        test: /\.js?$/,
        loader: 'babel-loader',
        query: {
          presets: ['es2015', 'react']
        },
        exclude: /node_modules/
      }
    ]
  },
  plugins: [
  ]
}
