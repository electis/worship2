* Cron example

```
0 1 * * 1-6 /venv/worship2/bin/python /www/worship2/create.py
0 6 * * 3,6 /venv/worship2/bin/python /www/worship2/stream.py
0 6 * * 1,2,4,5 /venv/worship2/bin/python /www/worship2/stream.py .env_vk
```
