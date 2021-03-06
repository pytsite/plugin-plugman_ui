"""PytSite Plugman UI Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load():
    from pytsite import lang
    from plugins import assetman

    lang.register_package(__name__)
    assetman.register_package(__name__)

    assetman.t_less(__name__)
    assetman.t_js(__name__)


def plugin_install():
    from plugins import assetman

    assetman.build(__name__)
    assetman.build_translations()


def plugin_load_uwsgi():
    from pytsite import plugman
    from plugins import settings, http_api
    from . import _settings_form, _http_api_controllers

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api_controllers.PostInstall,
                    'plugman_ui@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api_controllers.PostUninstall,
                    'plugman_ui@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api_controllers.PostUpgrade,
                    'plugman_ui@post_upgrade')

    if not plugman.is_dev_mode():
        # Settings
        settings.define('plugman', _settings_form.Form, 'plugman_ui@plugins', 'fa fa-plug', 'dev')
