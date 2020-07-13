# Program description
# xây dựng hệ thống check comment xấu:

#["bán hàng online", "gửi mình ảnh nude", ...]

# Write an API

# Thuật toán 
# Step 1: tách comment thành 1 list chữ bằng nltk
# Step 2: search xem trong list phân tách có từ nào trong banlist không

# TODO  
#	Reformat to MVC model
#	Clean up code
#	Optimize performance
#	Write Test Case


# GET /API/v1.0/nltk/filtercomment?word=porn&comment="link porn" HTTP/1.1
# Host: 127.0.0.1:5000

import flask
from flask import request
from flask import jsonify

app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Configuration
REDISCLIENT_HOST='localhost'
REDISCLIENT_PORT=6379,
REDISCLIENT_CHARSET="utf-8", 
REDISCLIENT_DECODE_RESPONSES=True,
REDISCLIENT_DB=0


# =====================
# The bag-of-words model
# import nltk
# nltk.download('punkt')
# SENT_DETECTOR = nltk.data.load('tokenizers/punkt/english.pickle')	
class CommentFilter(object):
	from nltk import word_tokenize
	import redis

	redisClient = redis.StrictRedis(host=REDISCLIENT_HOST,
	                                port=REDISCLIENT_PORT,
	                                charset=REDISCLIENT_CHARSET, 
	                                decode_responses=REDISCLIENT_DECODE_RESPONSES,
	                                db=REDISCLIENT_DB)
	ban_list = "ban_list"
	
	# Initiate key if needed
	# redisClient.lpush(ban_list, "nude", "XXX")

	def is_banned(self, comment):
		from nltk import word_tokenize

		comment_words = word_tokenize(comment)
		# for words in ban_list:
		for word in range(0, redisClient.llen(ban_list)):
			if word in comment_words:
				return "Comment has banned word"
		return "Comment does not have banned word"
		
	def mod_ban_list(self, word, add = 0):
		# TODO check input

		# add word to ban lists
		if add:
			if word in redisClient.mget(ban_list):
				return "Word is already in ban_list"
			else:
				redisClient.lpush(ban_list, word)
				return "Word added to ban list"

		# remove from ban lists
		else:
			try:
				redisClient.lrem(ban_list,0, word)
				return "Word removed from ban list"
			except:
				return "The word you are trying to remove doesn't exist in ban_list"

# =================
# Input
# -	word : no need string quote
# - comment : require string quote
# - add : 1 to add, 0 to remove

# Output
# -	conclusion
@app.route('/API/v1.0/nltk/filtercomment', methods=['GET'])
def filtercomment():

	args = request.args
	filter = CommentFilter()

	if "add" in args and "word" in args:
		return filter.mod_ban_list(args["word"], bool(args["add"]))

	if "comment" in args:
		return filter.is_banned(args["comment"])

	return "What the hell"

# =================
# Input
# -	None

# Output
# -	list of banned words
@app.route('/API/v1.0/nltk/check_ban_list', methods=['GET'])
def check_ban_list():
	filter = CommentFilter()

	for i in range(0, redisClient.llen(ban_list)):
		return jsonify(i)


@app.route('/', methods=['GET'])
def home():
	return "<h1>HOME PAGE</p>"

app.run()

