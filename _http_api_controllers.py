"""PytSite Plugman HTTP API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import plugman as _plugman, routing as _routing, reload as _reload
from plugins import auth as _auth


class PostInstall(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('plugman_ui@manage'):
            raise self.forbidden()

        plugin_name = self.arg('name')

        _plugman.install(plugin_name)
        _reload.reload()

        return _plugman.local_plugin_info(plugin_name, False)


class PostUninstall(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('plugman_ui@manage'):
            raise self.forbidden()

        _plugman.uninstall(self.arg('name'))
        _reload.reload()

        return {'status': True}


class PostUpgrade(_routing.Controller):
    def exec(self) -> dict:
        if not _auth.get_current_user().has_permission('plugman_ui@manage'):
            raise self.forbidden()

        _plugman.install(self.arg('name'))
        _reload.reload()

        return {'status': True}
