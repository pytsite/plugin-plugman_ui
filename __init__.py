"""PytSite Plugman UI Plugin
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import plugman, setup, update, console
    from plugins import assetman, permissions, settings, http_api
    from . import _settings_form, _http_api_controllers

    assetman.register_package(__name__)
    assetman.t_less(__name__ + '@**')
    assetman.t_js(__name__ + '@**')

    # HTTP API
    http_api.handle('POST', 'plugman/install/<name>', _http_api_controllers.PostInstall(),
                    'plugman_ui@post_install')
    http_api.handle('POST', 'plugman/uninstall/<name>', _http_api_controllers.PostUninstall(),
                    'plugman_ui@post_uninstall')
    http_api.handle('POST', 'plugman/upgrade/<name>', _http_api_controllers.PostUpgrade(),
                    'plugman_ui@post_upgrade')

    if not plugman.is_dev_mode():
        # Permissions
        permissions.define_permission('plugman_ui@manage', 'plugman_ui@plugin_management', 'app')

        # Settings
        settings.define('plugman', _settings_form.Form, 'plugman_ui@plugins', 'fa fa-plug', 'plugman_ui@manage')

        # Event handlers
        setup.on_setup(lambda: console.run_command('plugman:install', {'reload': False}), 999)
        update.on_update_after(lambda: console.run_command('plugman:update', {'reload': False}))


_init()
