import os
import pkgutil
import sys
from importlib import import_module

from django.conf import settings
from pkg_resources import iter_entry_points

from openslides.utils.main import (
    WINDOWS_PORTABLE_VERSION,
    detect_openslides_type,
    get_win32_portable_user_data_path,
)

plugins = {}


# Methods to collect plugins.

def collect_plugins_from_entry_points():
    """
    Collects all entry points in the group openslides_plugins from all
    distributions in the default working set and returns their module names as
    tuple.
    """
    return tuple(entry_point.module_name for entry_point in iter_entry_points('openslides_plugins'))


def collect_plugins_from_path(path):
    """
    Collects all modules/packages in the given `path` and returns a tuple
    of their names.
    """
    return tuple(x[1] for x in pkgutil.iter_modules([path]))


def collect_plugins():
    """
    Collect all plugins that can be automatically discovered.
    """
    # Collect plugins from entry points.
    collected_plugins = collect_plugins_from_entry_points()

    # Collect plugins in plugins/ directory of portable.
    if detect_openslides_type() == WINDOWS_PORTABLE_VERSION:
        plugins_path = os.path.join(
            get_win32_portable_user_data_path(), 'plugins')
        if plugins_path not in sys.path:
            sys.path.append(plugins_path)
        collected_plugins += collect_plugins_from_path(plugins_path)

    return collected_plugins


# Methods to retrieve plugins and their metadata.

def get_plugin(plugin):
    """
    Returns the imported module. The plugin argument must be a python dotted
    module path.
    """
    try:
        plugin = plugins[plugin]
    except KeyError:
        plugins[plugin] = import_module(plugin)
        plugin = get_plugin(plugin)
    return plugin


def get_plugin_verbose_name(plugin):
    """
    Returns the verbose name of a plugin. The plugin argument must be a python
    dotted module path.
    """
    plugin = get_plugin(plugin)
    try:
        verbose_name = plugin.get_verbose_name()
    except AttributeError:
        try:
            verbose_name = plugin.__verbose_name__
        except AttributeError:
            verbose_name = plugin.__name__
    return verbose_name


def get_plugin_description(plugin):
    """
    Returns the short descrption of a plugin. The plugin argument must be a
    python dotted module path.
    """
    plugin = get_plugin(plugin)
    try:
        description = plugin.get_description()
    except AttributeError:
        try:
            description = plugin.__description__
        except AttributeError:
            description = ''
    return description


def get_plugin_version(plugin):
    """
    Returns the version string of a plugin. The plugin argument must be a
    python dotted module path.
    """
    plugin = get_plugin(plugin)
    try:
        version = plugin.get_version()
    except AttributeError:
        try:
            version = plugin.__version__
        except AttributeError:
            version = 'unknown'
    return version


def get_plugin_urlpatterns(plugin):
    """
    Returns the urlpatterns object for a plugin. The plugin argument must be
    a python dotted module path.
    """
    plugin = get_plugin(plugin)
    try:
        urlpatterns = plugin.get_urlpatterns()
    except AttributeError:
        try:
            urlpatterns = plugin.urls.urlpatterns
        except AttributeError:
            urlpatterns = None
    return urlpatterns


def get_all_plugin_urlpatterns():
    """
    Helper function to return all urlpatterns of all plugins listed in
    settings.INSTALLED_PLUGINS.
    """
    urlpatterns = []
    for plugin in settings.INSTALLED_PLUGINS:
        plugin_urlpatterns = get_plugin_urlpatterns(plugin)
        if plugin_urlpatterns:
            urlpatterns += plugin_urlpatterns
    return urlpatterns
