var jsdom  = require('jsdom'),
    xmldom = require('xmldom'),
    fs     = require('fs'),
    path   = require('path'),
    html   = require('js-beautify').html;

function run(htmldir, outdir) {
  try {
    fs.mkdirSync(outdir);
  }
  catch (e) {}

  var xmldir = path.join(htmldir, 'xml');
  var files = fs.readdirSync(xmldir);

  var indexhtml = fs.readFileSync(path.join(htmldir, 'index.html'), {
    encoding: 'utf-8',
  });

  var css = null;

  for (var i = 0; i < files.length; i++) {
    console.log('Generating static page for ' + files[i]);

    // Load xml file
    var xmlfile = path.join(xmldir, files[i]);

    var x = fs.readFileSync(xmlfile, {
      encoding: 'utf-8',
    });

    var xmldoc = (new xmldom.DOMParser()).parseFromString(x);

    var doc = jsdom.jsdom(indexhtml, {
      features: {
        FetchExternalResources: ['script'],
        ProcessExternalResources: ["script"],
      },
    });

    if (doc.errors) {
      for (var e = 0; e < doc.errors.length; e++) {
        console.error(doc.errors[e].message);
        console.error(doc.errors[e].data);
      }

      process.exit(1);
    }

    var window = doc.defaultView;
    var $ = window.jQuery;

    var cldoc = window.cldoc;

    var name = files[i].substring(0, files[i].length - 4);

    cldoc.Page.pages[name] = {
      xml: $(xmldoc),
      html: null,
    };

    cldoc.Page.load(name);

    $('a').each(function (i, a) {
      a = $(a);

      var href = a.attr('href').replace(/::/g, '.');

      if (href.length == 0 || href[0] != '#') {
        return;
      }

      var parts = href.substring(1).split('/', 2);

      if (parts[0] == '') {
        parts[0] = 'index';
      }

      parts = parts.map(function (v) {
        return encodeURIComponent(v);
      });

      if (parts[0] == name) {
        href = '#';
      } else {
        href = parts[0] + '.html';

        if (parts.length > 1) {
          href += '#';
        }
      }

      if (parts.length > 1) {
        href += parts[1];
      }

      a.attr('href', href);
    });

    if (!css) {
      css = $('style').text();
    }

    $('script').remove();
    $('style').remove();

    // For now, the static version does not support searching
    $('#cldoc_search').remove();

    // Add simple link for stylesheet
    var link = $('<link/>', {
      rel: 'stylesheet',
      type: 'text/css',
      href: 'styles/cldoc.css',
    });

    $('head').append(link);

    // Write resulting html to <name>.html
    fs.writeFileSync(path.join(outdir, name + '.html'), html(jsdom.serializeDocument(doc), {
      max_preserve_newlines: 1
    }));
  }

  // Write css to styles/cldoc.css
  var stylesdir = path.join(outdir, 'styles');

  try {
    fs.mkdirSync(stylesdir);
  } catch (e) {}

  fs.writeFileSync(path.join(stylesdir, 'cldoc.css'), css + '#cldoc #cldoc_sidebar_items { bottom: 0; }');
}

module.exports = {
  run: run
};