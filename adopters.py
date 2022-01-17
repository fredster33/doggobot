#! /usr/bin/env python

from __future__ import unicode_literals
import mwclient
import mwparserfromhell
import datetime
from time import mktime

# Copyright CC-BY-SA 3.0 by Theopolisme. Edits to update to Python 3 and newer versions of libraries © EpicPupper. 

def active(user):
	"""Returns True if a user is active (i.e., last edit withinin
	XX months ago), False if inactive.
	"""
	contribs = site.usercontributions(user,limit=1)
	for contrib in contribs:
		timestamp = datetime.datetime.fromtimestamp(mktime(contrib[u'timestamp']))
		tdelta = now - timestamp
		if tdelta > datetime.timedelta(days=30):
			print("{0} hasn't edited for {1}, which is greater than 30 days.".format(user,tdelta))
			return False # user has not edited in past 30 days
		else:
			print("{0} last edited {1}, which is less than 30 days.".format(user,tdelta))
			return True

def main():
	global site,now
	site = mwclient.Site('en.wikipedia.org')
	site.login('username', 'password')
	now = datetime.datetime.now()

	page = site.Pages["Wikipedia:Adopt-a-user/Adoptee's Area/Adopters"]

	wikicode = mwparserfromhell.parse(page.text())
	for template in wikicode.filter_templates():
		if "Wikipedia:Adopt-a-user/Adopter Profile" in template.name:
			user = template.get('username').value.strip()
            # If user is not active
			if active(user) == False:
                # Add unavailable template parameter
				template.add('available','no')
                # Add bot-updated parameter
				template.add('bot-updated','yes')
            # If user is active and has been updated
			elif template.has_param('bot-updated') == True:
				template.add('available','yes')
	new_contents = str(wikicode)
	page.save(new_contents,summary="[[WP:BOT|Bot]]: Updating availabilities.")

if __name__ == '__main__':
	print("Powered on.")
	main()
