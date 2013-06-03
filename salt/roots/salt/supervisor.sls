supervisor:
  pkg:
    - installed
  service:
    - running
    - require:
      - pkg: supervisor

/etc/supervisor/conf.d/docs.conf:
  file:
    - managed
    - source: salt://supervisor/docs.conf

docs:
  supervisord:
    - running
    - restart: False
    - require:
      - service: supervisor
