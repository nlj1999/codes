import requests
import time
import sys
from bs4 import BeautifulSoup

def get_html(url):
	try:
		r = requests.get(url, timeout=30)
		r.raise_for_status()
		r.encoding = 'utf-8'
		return r.text
	except:
		return "ERROR"

def get_content(url):
	comments = []
	html = get_html(url)
	soup = BeautifulSoup(html, 'lxml')
	liTags = soup.find_all('li', attrs={'class':' j_thread_list clearfix'})
	for li in liTags:
		comment = {}
		try:
			comment['title'] = li.find('a', attrs={'class':'j_th_tit'}).text.strip()
			comment['link'] = "http://tieba.baidu.com" + li.find('a', attrs={'class':'j_th_tit'})['href']
			comment['name'] = li.find('span', attrs={'class':'tb_icon_author'}).text.strip()
			comment['time'] = li.find('span', attrs={'class':'pull-right is_show_create_time'}).text.strip()
			comment['replynum'] = li.find('span', attrs={'class':'threadlist_rep_num center_text'}).text.strip()
			comments.append(comment)
		except:
			print('a little problem')
	return comments

def Out2File(Dict):
	for comment in Dict:
		print('标题： {} \t 发帖人： {} \t 时间： {} \t 回复数： {} \t 链接： {} \n'.format(
			comment['title'],comment['name'],comment['time'],comment['replynum'],comment['link']))

def main(base_url, deep):
	for i in range(0, deep):
		url = base_url + '&pn=' + str(i * 50)
		content = get_content(url)
		Out2File(content)


base_url = "https://tieba.baidu.com/f?ie=utf-8&kw=" + sys.argv[1]
deep = int(sys.argv[2])

if __name__ == '__main__':
	main(base_url, deep)
			
