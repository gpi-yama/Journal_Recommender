#!/bin/sh
#isok=false
#while :
#do
    #cd /code/crawler/journal
    #scrapy crawl jfm
    #cd /code
    #mysqldump -u root --password=root journal > journal_backup.sql
    #echo "dump journal.sql"
python manage.py runserver 0.0.0.0:2715 &
    #if $isok; then
	#	break
    #fi
    #sleep 24h
    #killall python
    #echo "rerun"
#done
