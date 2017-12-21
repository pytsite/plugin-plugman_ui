"""PytSite Plugman UI Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _register_assetman_resources():
    from plugins import assetman

    if not assetman.is_package_registered(__name__):
        assetman.register_package(__name__)
        assetman.t_less(__name__)
        assetman.t_js(__name__)

    return assetman


def plugin_install():
    assetman = _register_assetman_resources()
    assetman.build(__name__)
    assetman.build_translations()


def plugin_load():
    from pytsite import lang

    lang.register_package(__name__)
    _register_assetman_resources()


def plugin_load_uwsgi():
    from pytsite import plugman
    from plugins import permissions, settings, http_api
    from . import _settings_form, _http_api_controllers

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api_controllers.PostInstall,
                    'plugman_ui@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api_controllers.PostUninstall,
                    'plugman_ui@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api_controllers.PostUpgrade,
                    'plugman_ui@post_upgrade')

    if not plugman.is_dev_mode():
        # Permissions
        permissions.define_permission('plugman_ui@manage', 'plugman_ui@plugin_management', 'app')

        # Settings
        settings.define('plugman', _settings_form.Form, 'plugman_ui@plugins', 'fa fa-plug', 'plugman_ui@manage')
