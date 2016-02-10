# -*- coding: utf-8 -*-
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

		all_vars = '\n'.join([k + '="' + str(v) + '"' for k,v in self.classconfig.iteritems()])
		open('/home/kiosk/.kiosk/browser.cfg', 'w').write(all_vars) #save
			