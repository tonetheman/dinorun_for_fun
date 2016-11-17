
import traceback,time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# this is advanced interation api!
from selenium.webdriver.common.action_chains import ActionChains

from PIL import Image
import base64, cStringIO

def log(*args):
	print time.ctime(),
	for a in args:
		print str(a),
	print

def get_section(img):
	# this section
	# is what I figured out by messing with it
	top = 60
	left = 170
	width = 1280
	height = 310

	box = (left,top,left+width,top+height)

	return img.crop(box)

def save_screenshot_now(browser, filename):
	img_data_base64 = browser.get_screenshot_as_base64()

	outf = open(filename,"wb")
	outf.write(base64.b64decode(img_data_base64))
	outf.close()
	
	inf = cStringIO.StringIO(base64.b64decode(img_data_base64))
	img = Image.open(inf)
	img = get_section(img)
	img.save("out.png")

def get_image(browser):
	img_data_base64 = browser.get_screenshot_as_base64()
	inf = cStringIO.StringIO(base64.b64decode(img_data_base64))
	img = Image.open(inf)
	return get_section(img)

def found_end_of_game(img):
	"""
		looks for top of G and two humps on M
		in GAME OVER
	"""
	# top of G in game over
	for i in range(446,460):
		_tmp = img.getpixel((i,95))
		if _tmp!=(83,83,83):
			return False	


	# first hump in M
	for i in range(536,541):
		_tmp = img.getpixel((i,95))
		if _tmp!=(83,83,83):
			return False

	# second hump in M	
	for i in range(551,556):
		_tmp = img.getpixel((i,95))
		if _tmp!=(83,83,83):
			return False	

	return True

def mainline():
	log("starting mainline")
	browser = None
	try:
		browser = webdriver.Chrome()
		browser.set_window_position(0,0)
		browser.set_window_size(800,800)
		time.sleep(5)

		# browser.get("http://google.com")
		browser.get("chrome://network-error/-106")

		log("getting runner canvas")

		runner_canvas = browser.find_element_by_class_name("runner-canvas")

		a = ActionChains(browser) \
			.click(runner_canvas) \
			.send_keys(" ")

		log("about to make him run...")
		# this starts the dino running
		a.perform()
	
		# create this and use it in a loop	
		a2 = ActionChains(browser) \
			.send_keys(" ")

		index = 0
		start_loop = time.time()
		while True:
			log("getting frame",index)
			img_frame = get_image(browser)

			# debug
			log("saving frame", index)
			img_frame.save("dbg%d.png" %(index,))
			index = index + 1

			log("looking for end of game")
			res = found_end_of_game(img_frame)
			log("found end of game", res)
	
			if res:
				log("stopping now found end of game in frame")
				break

			log("sleeping")
			time.sleep(0.1)
	
			log("jumping")
			a2.perform()

		# index = 0
		# log("starting range")
		# for i in range(5):
		#	time.sleep(1)
		#	a2.perform()
		#	# save_screenshot_now(browser, "%d.png" % (index,))
		#	index = index + 1

		# log("sleep 5...")
		# time.sleep(5)

		log("saving final shot")
		save_screenshot_now(browser, "final_screenshot.png")
	
		stop_loop = time.time()

		log("start", start_loop, "stop", stop_loop, "diff", (stop_loop-start_loop))
		log("index", index)
		log("index/time", 1.0*index/(stop_loop-start_loop))	
	except:
		traceback.print_exc()	
	finally:
		if browser is not None:
			browser.quit()

	log("fin")

if __name__ == "__main__":
	mainline()

