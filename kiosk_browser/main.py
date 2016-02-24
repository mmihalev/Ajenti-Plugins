# -*- coding: utf-8 -*-
import subprocess
from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

@plugin
class SanickioskScreensaverPrefs (SectionPlugin):
	default_classconfig = {
		'enable_browser': False,
		'home_url': 'http://locahost:8080',
	}
	classconfig_root = True

	def init(self):
		self.title = 'Режим Браузър'
		self.icon = 'globe'
		self.category = 'Kiosk'

		self.append(self.ui.inflate('kiosk_browser:main'))
		self.binder = Binder(self, self)
		self.binder.populate()

	@on('save', 'click')
	def save(self):
		self.binder.update()
		self.save_classconfig()
		self.context.notify('info', _('Настройките са запаметени. Моля, рестартирайте киоска.'))
		self.binder.populate()

		#all_vars = '\n'.join([k + '="' + str(v) + '"' for k,v in self.classconfig.iteritems()])
		for k,v in self.classconfig.iteritems():
		    if k == 'enable_browser':
			    enable_browser = "X-GNOME-Autostart-enabled=%s" % str(v).lower()
		    if k == 'home_url':
			    home_url = v.lower()
        
        if enable_browser == "X-GNOME-Autostart-enabled=true":
            ajenti_config = "/etc/ajenti/config.json"
            
            #Disable Video Mode
            subprocess.call(['sed', '-i', r's/\\"enable_videos\\": true/\\"enable_videos\\": false/g', ajenti_config])
            subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-videos.desktop"])
            
            #Disable Photo Mode
            subprocess.call(['sed', '-i', r's/\\"photos_enable\\": true/\\"photos_enable\\": false/g', ajenti_config])
            subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-photos.desktop"])
        
        cfg = ("[Desktop Entry]\n"
			"Type=Application\n"
			"Exec=chromium-browser --kiosk --no-first-run --disable-infobars --disable-session-crashed-bubble %s\n"
			"Hidden=false\n"
			"NoDisplay=false\n"
			"%s\n"
			"Name[en_US]=2-browser\n"
			"Name=2-browser\n"
			"Comment[en_US]=\n"
			"Comment=") % (home_url, enable_browser)
        
        open('/home/kiosk/.config/autostart/2-browser.desktop', 'w').write(cfg) #save
