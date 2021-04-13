import datetime
import requests,urllib
import time
import csv
import os
from settings import token as TOKEN

def url_to_id(group_url):
  global url
  url = group_url.replace('https://vk.com/', '')
  return url

def humantime_to_unixtime(input_data):
  date_time_obj = datetime.datetime.strptime(input_data, '%d.%m.%Y').date()
  unixtime = time.mktime(date_time_obj.timetuple())
  return unixtime

def parse_posts(url):
  token = TOKEN
  version = 5.92
  count = 100
  all_posts = []
  offset = 0
  parse_day = input('C какого дня парсить? Формат ДД.ММ.ГГГГ:\n').strip()#'11.04.2021'
  parse_begin = humantime_to_unixtime(parse_day)
  timestamp_enqd = input('До какого дня парсить? Формат ДД.ММ.ГГГГ:\n').strip()
  parse_end = humantime_to_unixtime(timestamp_enqd)
  start = datetime.datetime.now()

  #print(parse_begin, timestamp_end )

  while offset < 10000:
    response = requests.get('https://api.vk.com/method/wall.get',
                            params={
                              'access_token': token,
                              'v': version,
                              'domain': url_to_id(url),
                              'count': count,
                              'offset': offset
                            } 
    )
    data = response.json()['response']['items']
    #print(data[]['date'], parse_begin)
    #if data[10]['date'] < parse_begin:
    #  break
    #print(data)
    for i in range(1, len(data)):
      #print(i)

      if data[i]['date'] > parse_begin and data[i]['date'] < parse_end + 86000:
        all_posts.append(data[i])


    offset += 300
    #all_posts.extend(data)
    time.sleep(0.5)

  end = datetime.datetime.now()
  total = end - start
  print(total)
  return all_posts


def file_creater(all_posts):

  posts_count = 0
  for post in all_posts:
    try:
      if post['attachments'][0]['type']:
        img_url = post['attachments'][0]['photo']['sizes'][-1]['url']
        #print(post['attachments'][0]['photo'])
      else:
        img_url = 'pass'
    except:
      img_url = 'pass'
      pass

    posts_count += 1
    try:
      os.makedirs(f'images/images_{url}')    
      urllib.request.urlretrieve(img_url, f'images/images_{url}/img_name_{posts_count}.jpg')
      #print("Directory " + " Created ")
    except Exception as e:
      try:
        urllib.request.urlretrieve(img_url, f'images/images_{url}/img_name_{posts_count}.jpg')
      except Exception as e:
        pass
      #print("Directory " + " already exists")
    #print()   
    print(f'Записано {posts_count} постов')
    #time.sleep(0.1)




all_posts = parse_posts('https://vk.com/bfna40min')
file_creater(all_posts)
#all_posts = parse_posts('https://vk.com/ru9gag')
