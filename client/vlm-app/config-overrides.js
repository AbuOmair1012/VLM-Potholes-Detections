const webpack = require('webpack');

module.exports = function override(config) {
  config.resolve.fallback = {
    ...config.resolve.fallback,
    buffer: require.resolve('buffer/'),
    assert: require.resolve('assert/'),
    constants: require.resolve('constants-browserify'),
    stream: require.resolve('stream-browserify'),
    path: require.resolve('path-browserify'),
    process: require.resolve('process/browser'),
  };

  config.plugins = (config.plugins || []).concat([
    new webpack.ProvidePlugin({
      Buffer: ['buffer', 'Buffer'],
      process: 'process/browser',
    }),
  ]);

  return config;
};
