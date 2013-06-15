personalsite-installed:
  pip.installed:
    - editable: file:///vagrant
    - require:
      - pkg: python-pip

/etc/motd:
  file.managed:
    - source: salt://motd
