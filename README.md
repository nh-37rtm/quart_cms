

# Cms like using quart



## start


````bash
(venv) (venv) app@debian:/app/src$ python3 ./ep.py 
2024-09-13 10:43:50,834 root INFO  importing dependencies ...
2024-09-13 10:43:50,867 root INFO  generating json schema ...
2024-09-13 10:43:50,867 - INFO - app_context - generating json schema ...
2024-09-13 10:43:50,877 default INFO  starting application in debug mode ...
2024-09-13 10:43:50,877 - INFO - ep - starting application in debug mode ...
2024-09-13 10:43:50,877 asyncio DEBUG Using selector: EpollSelector
2024-09-13 10:43:50,877 - DEBUG - selector_events - Using selector: EpollSelector
 * Serving Quart app 'etp0'
 * Debug mode: True
 * Please use an ASGI server (e.g. Hypercorn) directly in production
 * Running on http://127.0.0.1:5000 (CTRL + C to quit)
2024-09-13 10:43:50,905 asyncio INFO  <Server sockets=(<asyncio.TransportSocket fd=6, family=2, type=1, proto=0, laddr=('127.0.0.1', 5000)>,)> is serving
2024-09-13 10:43:50,905 - INFO - base_events - <Server sockets=(<asyncio.TransportSocket fd=6, family=2, type=1, proto=0, laddr=('127.0.0.1', 5000)>,)> is serving
[2024-09-13 10:43:50 +0200] [8403] [INFO] Running on http://127.0.0.1:5000 (CTRL + C to quit)
2024-09-13 10:43:50,905 hypercorn.error INFO  Running on http://127.0.0.1:5000 (CTRL + C to quit)
2024-09-13 10:43:50,905 - INFO - logging - Running on http://127.0.0.1:5000 (CTRL + C to quit)
````