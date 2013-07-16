nodejs-ppas:
  pkgrepo.managed:
    - human_name: Node.js
    - ppa: chris-lea/node.js
    - require_in:
      - pkg: nodejs

nodejs:
  pkg:
    - installed
    - version: 0.10.12-1chl1~precise1

npm-packages:
  npm:
    - installed
    - names:
      - less
      - uglify-js
      - coffee-script
      - handlebars
    - require:
      - pkg: nodejs
