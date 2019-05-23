from flask import Flask

def create_app():
	from flask import abort
	from flask import request
	from flask import render_template
	app = Flask(__name__)

	@app.route('/<path:url>')
	def abort404(url):
		if url not in {'pic','996',''}:
			abort(404)
		else:
			pass	

	@app.route('/')
	def index():
		"""
		只有 Hello World 的首页
		:return:
		"""
		return "Hello, world!"

	# TODO: 捕获 404 错误，返回 404.html
	@app.errorhandler(404)
	def page_not_found(error):
		"""
		以此项目中的404.html作为此Web Server工作时的404错误页
		"""
		return render_template("404.html"),404

	# TODO: 完成接受 HTTP_URL 的 picture_reshape
	# TODO: 完成接受相对路径的 picture_reshape
	@app.route('/pic', methods=['GET'])
	def picture_reshape():
		"""
		**请使用 PIL 进行本函数的编写**
		获取请求的 query_string 中携带的 b64_url 值
		从 b64_url 下载一张图片的 base64 编码，reshape 转为 100*100，并开启抗锯齿（ANTIALIAS）
		对 reshape 后的图片分别使用 base64 与 md5 进行编码，以 JSON 格式返回，参数与返回格式如下
		
		:param: b64_url: 
			本题的 b64_url 以 arguments 的形式给出，可能会出现两种输入
			1. 一个 HTTP URL，指向一张 PNG 图片的 base64 编码结果
			2. 一个 TXT 文本文件的文件名，该 TXT 文本文件包含一张 PNG 图片的 base64 编码结果
				此 TXT 需要通过 SSH 从服务器中获取，并下载到`pandora`文件夹下，具体请参考挑战说明
		
		:return: JSON
		{
			"md5": <图片reshape后的md5编码: str>,
			"base64_picture": <图片reshape后的base64编码: str>
		}
		"""
		import PIL
		from PIL import Image
		import base64
		import hashlib
		import requests
		from flask import jsonify
		if request.method == 'GET':
			#text = request.args['b64_url']
			text = str(request.query_string, 'utf-8')
			#get original base64
			#if xxx.txt
			if "http" not in text:
				file0 = open(text, "rb")
				b64 = file0.read()
				file0.close()
			#if url
			else:
				b64 = requests.get(text).content()
			#decode to png
			imgdata = base64.b64decode(b64)  
			file1 = open("img.png","wb")  
			file1.write(imgdata)  
			file1.close()
			#reshape&save:
			img = Image.open("img.png")
			out = img.resize((100, 100),Image.ANTIALIAS)
			out.save("img-reshaped.png", "png")
			#get original bytes
			file2 = open("img-reshaped.png", "rb")
			originBytes = file2.read()
			file2.close()
			#change to b64
			bs64Code = str(base64.b64encode(originBytes), 'utf-8')
			#change to md5
			encoder = hashlib.md5()
			encoder.update(originBytes)#.encode(encoding='utf-8'))
			md5Code = encoder.hexdigest()
			dictionary = {"md5":md5Code,"base64_picture":bs64Code}
			return jsonify(dictionary)

	# TODO: 爬取 996.icu Repo，获取企业名单
	@app.route('/996')
	def company_996():
		"""
		从 github.com/996icu/996.ICU 项目中获取所有的已确认是996的公司名单，并

		:return: 以 JSON List 的格式返回，格式如下
		[{
			"city": <city_name 城市名称>,
			"company": <company_name 公司名称>,
			"exposure_time": <exposure_time 曝光时间>,
			"description": <description 描述>
		}, ...]
		"""
		import requests
		from flask import jsonify
		import re
		code = requests.get(r"https://github.com/996icu/996.ICU/blob/master/blacklist/README.md").content
		originalResult = re.findall(r'<td align="center">(.*)</td>',code.decode("utf-8"))[35::]
		ansList = []
		dictionary = {}
		for i in range(len(originalResult)):
			flag = i % 5
			item = originalResult[i]
			if flag == 0:
				dictionary.update({"city":item})
			elif flag == 1:
				templist = re.findall(r'>(.*)</a>',item)
				if len(templist) == 0:
					dictionary.update({"company":item})
				else:
					dictionary.update({"company":templist[0]})
			elif flag == 2:
				dictionary.update({"exposure_time":item})
			elif flag == 3:
				dictionary.update({"description":item})
			elif flag == 4:
				ansList.append(dictionary.copy())
				dictionary.clear()
		app.config['JSON_AS_ASCII'] = False
		return jsonify(ansList)

	return app

if __name__ == '__main__':
	app = create_app()
	app.run()