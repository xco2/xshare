source /home/xco2/miniconda3/bin/activate
cd /home/xco2/xshare/service
kill -9 $(ps -Alf|grep upload.py|grep -v grep| awk '{print $4}')
nohup python upload.py >> /home/xco2/xshare/service/flask.log 2>&1 &

