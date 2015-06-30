#!/usr/bin/env node

var path = require('path');
var fs   = require('fs');
var lib  = path.join(path.dirname(fs.realpathSync(__filename)), '../lib');

if (process.argv.length < 3) {
  console.error('Please specify the html output directory');
  process.exit(1);
}

if (process.argv.length < 4) {
  console.error('Please specify the static output directory');
  process.exit(1);
}

require(lib + '/cldoc-static').run(process.argv[2], process.argv[3]);