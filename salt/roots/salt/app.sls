personalsite-installed:
  pip.installed:
    - editable: file:///vagrant
    - require:
      - pkg: python-pip
