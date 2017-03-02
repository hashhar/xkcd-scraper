from requests import get
from random import randrange
from json import loads
from re import search
from PIL import Image, ImageDraw, ImageFont
from textwrap import wrap
import argparse
import os

# Let's make a class to hold everything
class xkcd_scraper:
	def __init__(self, download_dir):
		# Download_dir doesn't exist -> get out of there (may be a trap)
		if not os.path.exists(download_dir + os.path.sep):
			print("ERROR: ", "'" + download_dir + "', no such directory")
			raise SystemExit
		# If we don't have access to download_dir -> get out of there
		if not os.access(download_dir, os.W_OK):
			print("ERROR:", "'" + download_dir + "', permission denied")
			raise SystemExit
		# Set the variables if everything is good
		self.download_dir = download_dir
		self.append_title = False
		self.embed = False
		# Settings that control the embedded text appearance
		self.title_fontsize = 28
		self.alt_fontsize = 18
		self.line_offset = 10

	def download_json(self, comic_number):
		# Can this even happen
		if comic_number < 0:
			return None
		# Try to get the JSONs
		try:
			# Currently the JSONs are available at links like:
			# xkcd.com/comic_number/info.0.json and the latest one at
			# xkcd.com/info.0.json
			if comic_number == 0:
				return get("http://xkcd.com/info.0.json").json()
			else:
				return get(("http://xkcd.com/{0}/info.0.json").format(comic_number)).json()
		except (requests.exceptions.ConnectionError, ValueError):
			return None

	def add_text(self, image, title, alt, tfont = 'xkcd.ttf', afont = 'xkcd.ttf'):
		try:
			img = Image.open(image)
		except OSError:
			return

		tfont = ImageFont.truetype("xkcd.ttf", self.title_fontsize)
		afont = ImageFont.truetype("xkcd.ttf", self.alt_fontsize)
		# Compute the widths and heights for the title and alt
		twidth, theight = tfont.getsize(title)
		awidth, aheight = afont.getsize(alt)
		line_padding = 5
		# Get the object to draw upon
		draw = ImageDraw.Draw(img)
		lines = self.text_wrap(tfont, title, img.size[0])
		lheight = max([tfont.getsize(" ".join(i))[1] for i in lines])
		lheight_total = (lheight + line_padding) * (len(lines)) + line_padding * 4
		title_crop = (0, -1 * lheight_total, img.size[0], img.size[1])
		img = img.crop(title_crop)
		w, h = img.size
		old_h = h
		draw = ImageDraw.Draw(img)
		lheight_total = line_padding
		for i in lines:
			draw.text((w / 2 - tfont.getsize(" ".join(i))[0] / 2,
					  lheight_total),
					  " ".join(i),
					  font=tfont,
					  fill=0xffffff)
			lheight_total += lheight + line_padding
		lheight_total = line_padding
		lines = self.text_wrap(afont, alt, w)
		lheight = max([afont.getsize(" ".join(i))[1] for i in lines])
		lheight_total = lheight * len(lines)
		alt_crop = (0, 0, img.size[0],
					img.size[1] + lheight_total + (len(lines) + 3) * line_padding)
		img = img.crop(alt_crop)
		draw = ImageDraw.Draw(img)
		lheight_total = old_h + line_padding
		for i in lines:
			if not i:
				continue
			draw.text((w / 2 - afont.getsize(" ".join(i))[0] / 2,  lheight_total), " ".join(i), font=afont, fill=0xffffff)
			lheight_total += lheight + line_padding
		# Save all of the stuff we did
		img.save(image)

	def text_wrap(self, font, text, image_width, i = 0):
		lines = [[]]
		text = text.split(" ")
		while len(text) > 0:
			while len(text) > 0 \
					and font.getsize(" ".join(lines[i]))[0] < image_width:
				if font.getsize(text[0] + " " + " ".join(lines[i]))[0] \
						> image_width * 0.95:
					if len(lines[i]) == 0:
						text[0] = text[0][:len(text[0]) // 2 + 1] \
							+ " " + text[0][:len(text[0]) // 2 + 1:]
						text = text[0].split(" ") + text[1:]
					break
				lines[i].append(text[0])
				text.pop(0)
			i += 1
			lines.append([])
		sub = []
		for e, i in enumerate(lines):
			if font.getsize(" ".join(lines[e]))[0] > image_width:
				temp_str = ""
				for c in "".join(i):
					if font.getsize(temp_str + c)[0] > image_width:
						lines[i] = lines[i][:len(lines[i]) // 2] \
							+ lines[i][len(lines[i]) // 2:]
						break
					temp_str += c
				sub.append(temp_str)
				del lines[e]
		lines = [i for i in lines if len(i) != 0]
		for c in [i for i in sub if len(i) != 0]:
			lines.append(c)
		return lines

	def download_images(self, comic_number):
		# The object where we will write the image, will be used later
		images = []
		# Let's be careful about the 404 comic
		# You HAVE to see it though...  http://xkcd.com/404
		if comic_number == 404:
			print("You should try heading out to http://xkcd.com/404 yourself!")
			print("It's such a good one we couldn't manage to download it!")
			return
		if comic_number == 0:
			print("Fetching comic -> Latest".format(comic_number))
		else:
			print("Fetching comic -> {0}".format(comic_number))
		# Retrieve the JSON of the comic
		info = self.download_json(comic_number)
		# In case we failed to retrieve the JSON, abort mission
		if not info:
			print("ERROR:\nWhat we want you to think happenned -> The URL could not be reached!")
			print("What actually happenned -> The JSON associated with the comic could not be retrieved!")
			return
		# If we have got the JSON, lets get to work and extract relevant information
		title = info['safe_title']
		alt = info['alt']
		num = str(info['num'])
		url = info['img']
		date = info['day'] + "/" + info['month'] + "/" + info['year']
		# Let's decide the name we want to give to our downloaded images
		# Extract the file extension from the image url and append comic title
		if self.append_title == True:
			image = num + " - " + title + search("\.([a-z])+$", info['img']).group()
		else:
			image = num + search("\.([a-z])+$", info['img']).group()
		# Open the image file for writing
		with open(self.download_dir + '/' + image, 'wb') as image_file:
			# Get the image from the website
			srcimg = get(info['img'], stream = True)
			for block in srcimg.iter_content(1024):
				if block:
					image_file.write(block)
					image_file.flush()
			if self.embed and not search("\.gif", info['img']):
				print("Processing comic -> {0}".format(comic_number))
				self.add_text(self.download_dir+'/'+image, title, alt)

	def download_all(self):
		# We get the latest comic number from the download_json(0)['num'] and add 1
		# because range function is not inclusive
		for i in range(1, self.download_json(0)['num'] + 1):
			self.download_images(i)

	def download_random(self, iterations = 1):
		# Check if we have a connection by getting the JSON for the latest comic
		info = self.download_json(0)
		if not info:
			print("ERROR:\nWhat we want you to think happenned -> The URL could not be reached!")
			print("What actually happenned -> The JSON associated with the comic could not be retrieved!")
			return
		else:
			# Download as many random comics as requested
			for i in range(iterations):
				self.download_images(randrange(1, info['num'] + 1))

def main():
	# Let's add some command line arguments
	parser = argparse.ArgumentParser(description='Retrieve xkcd comics.', prefix_chars='-+')
	# Output directory argument
	parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', action='store', default='./', help='Change the output directory. Default is current directory')
	# The comic number argument
	parser.add_argument('N', type=int, nargs='*', help='An integer or set of integers greater than or equal to zero. Use 0 for latest comic.')
	# The range argument to help download multiple comics
	parser.add_argument('-r', '--range', action='store', metavar='N', type=int, nargs=2, help='Fetch comics within a certain range')
	# The all argument to download all comics
	parser.add_argument('-a', '--all', action='store_true', help='Fetch all comics')
	# The random argument
	parser.add_argument('-x' ,'--random', metavar='ITERATIONS', type=int, help='Fetch random comics', nargs='?', const=1)
	# The append comic title argument
	parser.add_argument('-t', '--title', action='store_true', help='Appends the comic title to the filename')
	# The embed comic title and alt text in the image argument
	parser.add_argument('-e', '--embed', action='store_true', help='Embeds the comic title and alt text to the comic image (unless its a gif)')

	args = parser.parse_args()
	x = xkcd_scraper(args.output_dir)

	# Let us try and make sense of the arguments passed
	if args.title:
		x.append_title = True
	if args.embed:
		x.embed = True
	# Range is pretty stand-alone
	if args.range:
		if args.N or args.random or args.all:
			raise argparse.ArgumentTypeError("You are confusing me... Please avoid using random, all or specific comic numbers with the range option.")
		else:
			# Download all the comics in the specified range
			for i in range(args.range[0], args.range[1] + 1):
				x.download_images(i)
			return
	# They want to download all comics
	if args.all:
		if args.N or args.random:
			raise argparse.ArgumentTypeError("You are confusing me... Random and individual comics numbers confuse me when you tell me to download all comics.")
		return x.download_all()
	# They want a random one (they think it's random but we know better)
	if args.random:
		if args.N:
			raise argparse.ArgumentTypeError("You are confusing me... How can I get a random comic for you if you keep telling me which one to download.")
		return x.download_random(args.random)
	else:
		# They obviously failed to provide an argument, let's help them
		if not args.N:
			parser.print_help()
		# They have specified specific comics, lets go get them
		for i in args.N:
			x.download_images(i)
		return

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		raise SystemExit
