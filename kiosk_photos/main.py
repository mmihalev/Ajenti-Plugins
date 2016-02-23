# -*- coding: utf-8 -*-
import subprocess
from ajenti.api import *
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

@plugin
class SanickioskScreensaverPrefs (SectionPlugin):
	default_classconfig = {
		'photos_enable': False,
	}
	classconfig_root = True

	def init(self):
		self.title = 'Режим Снимки'
		self.icon = 'picture'
		self.category = 'Kiosk'

		self.append(self.ui.inflate('kiosk_photos:main'))
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
            if k == 'photos_enable':
                photos_enable = "X-GNOME-Autostart-enabled=%s" % str(v).lower()
        
        if photos_enable == "X-GNOME-Autostart-enabled=true":
            ajenti_config = "/etc/ajenti/config.json"
            
            #Disable Browser Mode
            subprocess.call(['sed', '-i', r's/\\"enable_browser\\": true/\\"enable_browser\\": false/g', ajenti_config])
            subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-browser.desktop"])
            
            #Disable Video Mode
            subprocess.call(['sed', '-i', r's/\\"enable_videos\\": true/\\"enable_videos\\": false/g', ajenti_config])
            subprocess.call(['sed', '-i', r's/X-GNOME-Autostart-enabled=true/X-GNOME-Autostart-enabled=false/g', "/home/kiosk/.config/autostart/2-videos.desktop"])
            
        cfg = ("[Desktop Entry]\n"
            "Type=Application\n"
            "Exec=feh --recursive --quiet --randomize --full-screen --borderless --reload 300 --slideshow-delay 10 --no-menus --auto-zoom --hide-pointer /home/kiosk/Photos/\n"
            "Hidden=false\n"
            "NoDisplay=false\n"
            "%s\n"
            "Name[en_US]=2-photos\n"
            "Name=2-photos\n"
            "Comment[en_US]=\n"
            "Comment=") % (photos_enable)
            
		open('/home/kiosk/.config/autostart/2-photos.desktop', 'w').write(cfg) #save

