source /home/xco2/miniconda3/bin/activate
cd /home/xco2/xshare/service
#kill -9 $(ps aux | grep 'cyc_YunFu.py' | awk '{print $2}')
nohup python upload.py >> /home/xco2/xshare/service/flask.log 2>&1 &
#bash /home/opt/cychome/PyFlaskYunFu/nohup_update.sh
#tail -f /home/opt/cychome/PyFlaskYunFu.log
