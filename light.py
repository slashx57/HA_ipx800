# -*- coding: utf-8 *-*

import logging

import voluptuous as vol
from . import DOMAIN

# Import the device class from the component that you want to support
from homeassistant.components.light import ATTR_BRIGHTNESS, SUPPORT_BRIGHTNESS, PLATFORM_SCHEMA, LightEntity
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_ENABLED_VIRTANA = 'enabled_virtualanalogs'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Optional(CONF_ENABLED_VIRTANA): list
})


def setup_platform(hass, config, add_devices, discovery_info=None):
  """Setup the IPX800 Light platform."""

  _LOGGER.debug("Entering light.setup_platform")
  # Assign configuration variables. 
  enabled_virtana = config.get(CONF_ENABLED_VIRTANA)

  ipxdata = hass.data[DOMAIN]
  if ipxdata.update() == None:
    _LOGGER.warning("update failed")
    return 

  if enabled_virtana != None and len(enabled_virtana) > 0:
    # Instanciate IPXRelays
    virt_analogs = []
    for r in enabled_virtana:
      if ipxdata.virt_analogs!=None and len(ipxdata.virt_analogs)>=r :
        virt_analogs.append(ipxdata.virt_analogs[r-1])
      else:
        _LOGGER.warning("Requested virtual analog %i does not exists", r)

    # Add IPX800Light devices
    if (virt_analogs):
      add_devices(IPX800Light(virt_analog) for virt_analog in virt_analogs)

class IPX800Light(LightEntity):
  """Representation of a virtual analog of IPX"""

  def __init__(self, obj):
    """Initialize an IPX800Light."""
    self._obj = obj
    self._brightness = None
    self._supported_features = SUPPORT_BRIGHTNESS
    _LOGGER.debug(f"[light.{obj.name}] added")

  @property
  def name(self):
    """Return the display name of this light."""
    return "ipx800_" + self._obj.name

  @property
  def supported_features(self):
    """Flag supported features."""
    return self._supported_features

  @property
  def brightness(self):
      return self._brightness

  @property
  def is_on(self):
    """Return true if light is on."""
    return self._brightness!=0

  def turn_on(self, **kwargs):
    """Instruct the light to turn on.
    """
    if ATTR_BRIGHTNESS in kwargs:
      self._brightness = kwargs[ATTR_BRIGHTNESS]
    else:
      self._brightness = 255
    self._obj.set(self._brightness)

  def turn_off(self, **kwargs):
    """Instruct the light to turn off."""
    self._obj.set(0)

  def update(self):
    """Fetch new state data for this light.

    This is the only method that should fetch new data for Home Assistant.
    """
    self._brightness = self._obj.state
