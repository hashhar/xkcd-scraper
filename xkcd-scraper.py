import requests
from requests import get
from random import randrange
from json import loads
from re import search
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
		image = num + " - " + title + search("\.([a-z])+$", info['img']).group()
		# Open the image file for writing
		with open(self.download_dir + '/' + image, 'wb') as image_file:
			# TODO: Write code to manipulate the image
			# Get the image from the website
			srcimg = get(info['img'], stream = True)
			for block in srcimg.iter_content(1024):
				if block:
					image_file.write(block)
					image_file.flush()

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
	parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', action="store", default='./', help='Change the output directory. Default is current directory')
	# The comic number argument
	parser.add_argument('N', type=int, nargs='*', help='An integer or set of integers greater than or equal to zero')
	# The range argument to help download multiple comics
	parser.add_argument('-r', '--range', action="store", metavar='N', type=int, nargs=2, help='Fetch comics within a certain range')
	# The all argument to download all comics
	parser.add_argument('-a', '--all', action='store_true', help='Fetch all comics')
	# The random argument
	parser.add_argument('-x' ,'--random', metavar='ITERATIONS', type=int, help='Fetch random comics', nargs='?', const=1)

	args = parser.parse_args()
	x = xkcd_scraper(args.output_dir)

	# Let us try and make sense of the arguments passed
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