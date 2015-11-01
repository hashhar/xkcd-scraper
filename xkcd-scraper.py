from requests import get
import argparse
import os

# Let's make a class to hold everything
class xkcd_scraper:
	# ================================================================================
	# Let's initialise (this is analogous to constructors in C++)
	# self is similar to this variable in C#
	def __init__(self, download_dir):
		# If the download dir doesn't exist, we should get out of there (may be a trap)
		if not os.path.exists(download_dir + os.path.sep):
			print("Error:", "'" + download_dir + "', no such directory")
			raise SystemExit
		# If we don't have access to the download dir, they are probably messing with us. Let's get out.
		if not os.access(download_dir, os.W_OK):
			print("Error:", "'" + download_dir + "', permission denied")
			raise SystemExit
		# Set the download_dir if everything is good
		self.download_dir = download_dir
	
	# ================================================================================
	# Let's download the comic images
	def download_images(self, comic_number)
		# List for some purpose. I forgot why.
		images = []
		# Let's be careful about the 404 comic (you have to see it though... http://xkcd.com/404
		if comic_number == 404
			# Some intrigue for the user
			print("You should try heading out to http://xkcd.com/404 yourself! It's such a good joke we couldn't manage to download it!")
			# But we know better than to download it
			return
		
		# 0 is used to refer to the latest comic
		if comic_number == 404:
			print("Fetching comic -> Latest".format(comic_number))
		else:
			# The {0} is a positional argument and the .format method will replace it with the first argument
			print("Fetching comic -> {0}".format(comic_number))
		# For fetching a comic, we nedd to download it's JSON provided by xkcd
		info = self.download_json(comic_number)
		# In case we failed to retrieve the JSON, we say so
		if not info:
			print("ERROR: The JSON associated with the comic could not be retrieved")
			# We cannot do anything now
			return
		# If we have got the JSON, lets get to work and extract relevant information
		# FIXME: UPDATE THE CODE BELOW WHEN THE JSON FORMATS CHANGE
		# Title of the comic
		title = info['safe_title']
		# The alt text of the comic
		alt = info['alt']
		# The number of the comic
		num = str(info['num'])
		# URL of the comic image
		url = info['img']
		# The date the comic was released
		date = info['day'] + "/" + info['month'] + "/" + info['year']
		# Let's decide the name we want to give to our downloaded images
		# I know RegEx!!!
		# Search for a string with a leading dot and return the string (We are basically extracting the file extension from the image url and appending it to the comic number to get something like 614.png for comic 614
		# Feel free to open the exampleJSON.json file and run the RegEx on it to be sure
		image = num + search("\.([a-z])+$", info['img']).group()
		# Open the image file for writing in binary mode
		with open(self.download_dir + '/' + image, 'wb') as image_file:
			# TODO: Write code to manipulate the image
	
	# ================================================================================
	def download_json(self, comic_number):
		# Can this even happen
		if comic_number < 0:
			return None
		# Try to get the JSONs
		try:
			# Currently the JSONs are available at links like: xkcd.com/comic_number/info.0.json with the exception of the first comic
			if comic_number == 0:
				return get("http://xkcd.com/info.0.json").json()
			else:
				return get("http://xkcd.com/{0}/info.0.json").format(comic_number)).json()
		except (requests.exceptions.ConnectionError, ValueError):
			return None
	
# ================================================================================
# Our code's execution starts here
def main():
	# Let's add some command line arguments
	parser = argparse.ArgumentParser(description='Retrieve xkcd comics.', prefix_chars='-+')
	parser.add_argument('-o', '--output-dir', metavar='DIRECTORY', action='store', default='./' help='Change the output directory. Default: current directory')
	parser.add_argument('N', type=int, nargs='*', help='An integer or set of integers greater than or equal to zero')
	parser.add_argument('-r', '--range', action="store", metavar='N', type=int, nargs=2, help='Fetch comics within a certain range')
	
	# Parse the arguments
	args = parser.parse_args()
	
	# Make an instance of our class
	x = xkcd_scraper(args.output_dir)
	
	# Let us try and make sense of the arguments passed
	# They want to download all comics, so they must not use the N option together with it
	if args.all:
		if args.N:
			raise argparse.ArgumentTypeError("You are confusing me... If you want to download all comics (yes, we know because you used the --all flag), you should not pass the comic number")
		return x.download_all(args.download_only)
	# They want to download a specific comic
	else:
		# If they forgot to mention which one, give them help
		if not args.N:
			parser.print_help()
		# If they did not forget, let's grant them their wish
		for i in args.N:
			x.download_images(i, args.download_only)
		return
	
# I honestly copied the below snippet and don't know what it EXACTLY does
if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		raise SystemExit