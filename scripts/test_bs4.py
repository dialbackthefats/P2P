from bs4 import BeautifulSoup

html = """
<html>
<head><title>黑马程序员</title></head>
<body>
<p id="test01">软件测试</p>
<p id="test02">2020年</p>
<a href="/api.html">接口测试</a>
<a href="/web.html">Web自动化测试</a>
<a href="/app.html">APP自动化测试</a>
</body>
</html>
"""
# 初始化soup对象，解析后的html
soup = BeautifulSoup(html, 'html.parser')
# 获取title的对象
print(soup.title)
# 获取title的标签名称
print(soup.title.name)
# 获取title的值
print(soup.title.string)
# 获取标签对象
print(soup.p)
# 获取所有的p的对象
print(soup.find_all('p'))
# 获取第一个p标签的id的属性
print(soup.p['id'])

# 打印出所有a标签的href属性的值和a标签的值
for x in soup.find_all('a'):
    print("href={} text={}".format(x['href'], x.string))