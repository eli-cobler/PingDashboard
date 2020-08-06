# This script simply creates the cronjob for the uptime_service script

# Default path to root user cron jobs
# /var/spool/cron/crontabs/root

root_cron_job_file = '/var/spool/cron/crontabs/root'
f = open(root_cron_job_file, 'a+')
f.write('* * * * * cd /apps && /apps/venv/bin/python /apps/app_repo/ping_dashboard/services/uptime_service.py >> /apps/logs/ping_dashboard/app_log/uptime_service.log 2>&1')