/home/vagrant/.profile:
  file.managed:
    - source: salt://.profile
    - template: jinja
    - context:
      settings_file: {{ pillar['personalsite_settings_file'] }}
    - user: vagrant
    - group: vagrant
