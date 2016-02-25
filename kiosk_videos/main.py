# -*- coding: utf-8 -*-
import subprocess
from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

@plugin
class SanickioskScreensaverPrefs (SectionPlugin):
	default_classconfig = {
		    'enable_videos': False,
    		'video_volume': 50
	}
	classconfig_root = True

	def init(self):
		self.title = 'Режим Видео'
		self.icon = 'facetime-video'
		self.category = 'Kiosk'

		self.append(self.ui.inflate('kiosk_videos:main'))
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
		    if k == 'enable_videos':
			enable_videos = "X-GNOME-Autostart-enabled=%s" % str(v).lower()
		    if k == 'video_volume':
			video_volume = v.lower()
		
		if enable_videos == "X-GNOME-Autostart-enabled=true":
		    ajenti_config = "/etc/ajenti/config.json"
		    
		    #Disable Browser Mode
		    subprocess.call(['sed', '-i', r's/\\"enable_browser\\": true/\\"enable_browser\\": false/g', ajenti_config])
		    subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-browser.desktop"])

		    #Disable Photo Mode
		    subprocess.call(['sed', '-i', r's/\\"photos_enable\\": true/\\"photos_enable\\": false/g', ajenti_config])
		    subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-photos.desktop"])

		cfg = ("[Desktop Entry]\n"
		    "Type=Application\n"
		    "Exec=/home/kiosk/.kiosk/videos.sh %s\n"
		    "Hidden=false\n"
		    "NoDisplay=false\n"
		    "%s\n"
		    "Name[en_US]=2-videos\n"
		    "Name=2-videos\n"
		    "Comment[en_US]=\n"
		    "Comment=") % (video_volume, enable_videos)
		    		    
		open('/home/kiosk/.config/autostart/2-videos.desktop', 'w').write(cfg) #save

