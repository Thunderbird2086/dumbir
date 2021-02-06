"""Config flow for dumbIR integration."""
import logging
from os import listdir, path
from pprint import pformat

import voluptuous as vol

from homeassistant import config_entries, core, exceptions

from .const import ( # pylint:disable=unused-import
    CONF_IRCODES,
    CONF_POWER_SENSOR,
    CONF_REMOTE,
    CONF_TEMPERATURE_SENSOR,
    DOMAIN,
    IRCODES_ROOT_DIR,
    PLATFORM_TO_ADD,
)
from . import PLATFORMS  # pylint:disable=unused-import

_LOGGER = logging.getLogger(__name__)

_OPTIONAL_TEMP_SENSOR = ['climate']
_STEP_USER_DATA_SCHEMA = {
    vol.Required(PLATFORM_TO_ADD, default=PLATFORMS[0]): vol.In(PLATFORMS)
}

_STEP_ENTITY_DATA_SCHEMA = {
    vol.Required("name"): str,
    vol.Required(CONF_REMOTE): str, #TODO list of remotes
    vol.Required(CONF_IRCODES): vol.In([]),
    vol.Optional(CONF_POWER_SENSOR): str #TODO list of sensors
}


def validate_input(user_input, platform):
    """Validate the user input allows us to connect."""
    # TODO check if remote exists
    
    # TODO check if power sensor exists and supports stage of on/off

    # TODO check if temperature sensor exist

    ir_codes = path.join(IRCODES_ROOT_DIR,
                         platform,
                         user_input[CONF_IRCODES])
    user_input.update({CONF_IRCODES: ir_codes,
                       PLATFORM_TO_ADD: platform
                      })

    return user_input


def update_schema(data_schema, platform):
    """Update schema values"""
    dumbir_path = path.join(IRCODES_ROOT_DIR, platform)
    ircodes = [f for f in listdir(dumbir_path) if f.endswith('yaml')]
    data_schema.update(
        { vol.Optional(CONF_IRCODES): vol.In(ircodes),
        }
    )

    if platform in _OPTIONAL_TEMP_SENSOR:
        data_schema.update(
            { vol.Optional("temp_sensor"): str
            }
        )

    return data_schema


class DumbIRConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for dumbIR."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_ASSUMED
    def __init__(self):
        self.platform = None

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=vol.Schema(_STEP_USER_DATA_SCHEMA)
            )

        self.platform = user_input[PLATFORM_TO_ADD]
        data_schema = update_schema(_STEP_ENTITY_DATA_SCHEMA,
                                    self.platform)
        _LOGGER.debug("data_schema : %s", data_schema)

        return self.async_show_form(
            step_id="entity", data_schema=vol.Schema(data_schema)
        )

    async def async_step_entity(self, user_input=None):
        """Handle the initial step."""
        _LOGGER.debug("entity - user_input: %s", user_input)

        errors = {}

        try:
            config = validate_input(user_input, self.platform)
        except InvalidRemote:
            errors["base"] = "invalid_remote"
        except InvalidPowerSensor:
            errors["base"] = "invalid_power_sensor"
        except InvalidTemperatureSensor:
            errors["base"] = "invalid_temperature_sensor"
        except Exception:  # pylint: disable=broad-except
            _LOGGER.exception("Unexpected exception")
            errors["base"] = "unknown"
        else:
            return self.async_create_entry(title=config['name'],
                                           data=config)

        data_schema = update_schema(_STEP_ENTITY_DATA_SCHEMA,
                                    self.platform)
        return self.async_show_form(
            step_id="entity",
            data_schema=vol.Schema(data_schema), errors=errors
        )


class InvalidIrCodesFile(exceptions.HomeAssistantError):
    """Error to indicate invalid ir codes file."""


class InvalidRemote(exceptions.HomeAssistantError):
    """Error to indicate invalid remote."""


class InvalidPowerSensor(exceptions.HomeAssistantError):
    """Error to indicate invalid power sensor."""


class InvalidTemperatureSensor(exceptions.HomeAssistantError):
    """Error to indicate invalid temperature sensor."""
