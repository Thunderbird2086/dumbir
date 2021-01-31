"""The dumbIR integration."""
import logging
import os.path
import yaml

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    PLATFORM_TO_ADD
)

_LOGGER = logging.getLogger(__name__)
PLATFORMS = ["climate", "light", "media_player"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the dumbIR component."""
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up dumbIR from a config entry."""
    # TODO Store an API object for your platforms to access
    # hass.data[DOMAIN][entry.entry_id] = MyApi(...)

    _LOGGER.debug("async_setup_entry: entry.data=(%s)", entry.data)
    component = entry.data[PLATFORM_TO_ADD]
    hass.data[DOMAIN][entry.entry_id] = component
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, component)
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    _LOGGER.debug("async_unload: entry.data=(%s)", entry.data)
    component = entry.data[PLATFORM_TO_ADD]
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, component)
            ]
        )
    )

    _LOGGER.debug("async_unload: unload_ok=(%s)", unload_ok)
    _LOGGER.debug("async_unload: unload_ok=(%s)", type(unload_ok))
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok


def load_ircodes(hass, ircodes_path):
    """load ircodes"""
    if ircodes_path.startswith("/"):
        ircodes_path = ircodes_path[1:]

    ir_codes_path = hass.config.path(ircodes_path)

    if not os.path.exists(ir_codes_path):
        _LOGGER.error("The ir code file was not found. (%s)", ir_codes_path)
        return None

    with open(ir_codes_path, 'r') as f:
        ir_codes = yaml.load(f, Loader=yaml.SafeLoader)

    if not ir_codes:
        _LOGGER.error("The ir code file is empty. (%s)", ir_codes_path)

    return ir_codes


async def send_command(hass, remote, payload):
    """send command to broadlink remote"""
    if type(payload) is not str:
        # get an element from the array
        for ite in payload:
            # send a command
            await send_command(hass, remote, ite)
        return

    if not payload.startswith('b64:'):
        payload = ':'.join(('b64', payload))

    service_data_json = {'entity_id':  remote,
                         'command': payload}
    _LOGGER.debug("json: %s", service_data_json)

    await hass.services.async_call('remote', 'send_command',
                                   service_data_json)
