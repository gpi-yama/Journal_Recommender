# Journal_Recommender
Journal Recommender

# Usage

### Preparation

First of all, please make docker image   
```docker build -t django:v0 .```  
  
Second, please run docker container  
```docker run -itd --net=host -p 2715:2715 -v /home/yourname/Journal_Recommender/src:/code --name=jrecom django:v0```  
  
Thirdly, please attach docker container  
```docker exec -it jrecom bash ```   
  
and make mysql database (journal)  
```mysql -u root --password=root ```  
  
and create db  
```create database journal;```


### Run scrapy

pwd == /code/crawler/journal  
  
please run crawler  
```scrapy crawl jfm```   
  
or import journal.sql to db  
```mysql -u root --password=root journal < journal.sql```



### Run server
```python manage.py runserver 0.0.0.0:2715```


### Release  
2019.6.5  
AND search imlpement  
Recommender implement  