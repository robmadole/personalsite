python-dev:
  pkg.installed

python-pip:
  pkg.installed

fabric:
  pip.installed:
    - names:
      - fabric
      - sphinx
      - watchdog
    - download_cache: /home/vagrant/.pip-cache
    - require:
      - pkg: python-pip
