"""
Simple platform to control LOCALLY Tuya switch devices.

Sample config yaml

switch:
  - platform: localtuya
    host: 192.168.0.1
    local_key: 1234567891234567
    device_id: 12345678912345671234
    name: tuya_01
"""
import voluptuous as vol
from homeassistant.components.switch import SwitchDevice, PLATFORM_SCHEMA
from homeassistant.const import (CONF_HOST, CONF_ID, CONF_SWITCHES, CONF_FRIENDLY_NAME, CONF_ICON, CONF_NAME)
import homeassistant.helpers.config_validation as cv
from time import time
from threading import Lock

REQUIREMENTS = ['pytuya==7.0.4']

CONF_DEVICE_ID = 'device_id'
CONF_LOCAL_KEY = 'local_key'
CONF_PROTOCOL_VERSION = 'protocol_version'

DEFAULT_ID = '1'
DEFAULT_PROTOCOL_VERSION = 3.3

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_ICON): cv.icon,
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_DEVICE_ID): cv.string,
    vol.Required(CONF_LOCAL_KEY): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_PROTOCOL_VERSION, default=DEFAULT_PROTOCOL_VERSION): vol.Coerce(float),
    vol.Optional(CONF_ID, default=DEFAULT_ID): cv.string,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up of the Tuya switch."""
    from . import pytuya

    switches = []
    pytuyadevice = pytuya.OutletDevice(config.get(CONF_DEVICE_ID), config.get(CONF_HOST), config.get(CONF_LOCAL_KEY))
    pytuyadevice.set_version(float(config.get(CONF_PROTOCOL_VERSION)))
    
    outlet_device = TuyaCache(pytuyadevice)
    switches.append(
            TuyaDevice(
                outlet_device,
                config.get(CONF_NAME),
                config.get(CONF_ICON), 
                config.get(CONF_ID)
            )
    )

    add_devices(switches)

class TuyaCache:
    """Cache wrapper for pytuya.OutletDevice"""

    def __init__(self, device):
        """Initialize the cache."""
        self._cached_status = ''
        self._cached_status_time = 0
        self._device = device
        self._lock = Lock()

    def __get_status(self, switchid):
        for i in range(20):
            try:
                status = self._device.status()['dps'][switchid]
                return status
            except ConnectionError:
                if i+1 == 5:
                    raise ConnectionError("Failed to update status.")

    def set_status(self, state, switchid):
        """Change the Tuya switch status and clear the cache."""
        self._cached_status = ''
        self._cached_status_time = 0
        for i in range(20):
            try:
                return self._device.set_status(state, switchid)
            except ConnectionError:
                if i+1 == 5:
                    raise ConnectionError("Failed to set status.")

    def status(self, switchid):
        """Get state of Tuya switch and cache the results."""
        self._lock.acquire()
        try:
            now = time()
            if not self._cached_status or now - self._cached_status_time > 30:
                self._cached_status = self.__get_status(switchid)
                self._cached_status_time = time()
            return self._cached_status
        finally:
            self._lock.release()

class TuyaDevice(SwitchDevice):
    """Representation of a Tuya switch."""

    def __init__(self, device, name, icon, switchid):
        """Initialize the Tuya switch."""
        self._device = device
        self._name = name
        self._state = False
        self._icon = icon
        self._switch_id = switchid

    @property
    def name(self):
        """Get name of Tuya switch."""
        return self._name

    @property
    def is_on(self):
        """Check if Tuya switch is on."""
        return self._state

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    def turn_on(self, **kwargs):
        """Turn Tuya switch on."""
        self._device.set_status(True, self._switch_id)

    def turn_off(self, **kwargs):
        """Turn Tuya switch off."""
        self._device.set_status(False, self._switch_id)

    def update(self):
        """Get state of Tuya switch."""
        status = self._device.status(self._switch_id)
        self._state = status

