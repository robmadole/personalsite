python-dev:
  pkg.installed

python-pip:
  pkg.installed

python-tools:
  pip.installed:
    - names:
      - fabric
      - sphinx
      - watchdog
      - nose
      - coverage
      - mock
      - beautifulsoup4
    - download_cache: /home/vagrant/.pip-cache
    - require:
      - pkg: python-pip
