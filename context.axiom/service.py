import xbmc
import xbmcaddon

properties = [
    "context.axiom.quickResume",
    "context.axiom.shuffle",
    "context.axiom.playFromRandomPoint",
    "context.axiom.rescrape",
    "context.axiom.rescrape_ss",
    "context.axiom.sourceSelect",
    "context.axiom.findSimilar",
    "context.axiom.browseShow",
    "context.axiom.browseSeason",
    "context.axiom.traktManager",
]


class PropertiesUpdater(xbmc.Monitor):
    def __init__(self):
        super().__init__()
        self.addon = xbmcaddon.Addon()
        self._update_window_properties()

    def __del__(self):
        del self.addon

    def onSettingsChanged(self):
        self._update_window_properties()

    def _update_window_properties(self):
        for prop in properties:
            setting = self.addon.getSetting(prop)
            if setting == "false":
                xbmc.executebuiltin(f"SetProperty({prop},{setting},home)")
            else:
                xbmc.executebuiltin(f"ClearProperty({prop},home)")
            xbmc.log(f'Context menu item {"disabled" if setting == "false" else "enabled"}: {prop}')


xbmc.log("context.axiom service: starting", xbmc.LOGINFO)

try:
    # start monitoring settings changes events
    properties_monitor = PropertiesUpdater()

    # wait until abort is requested
    properties_monitor.waitForAbort()
except Exception as e:
    xbmc.log(f"context.axiom service: error - {e}", xbmc.LOGERROR)
finally:
    del properties_monitor

xbmc.log("context.axiom service: stopped", xbmc.LOGINFO)
