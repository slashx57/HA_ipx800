# -*- coding: utf-8 *-*

import sys
import logging
import time
from datetime import timedelta
from threading import Lock
from . import DOMAIN
import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.binary_sensor import DEVICE_CLASSES_SCHEMA, PLATFORM_SCHEMA, BinarySensorDevice
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_SCAN_INTERVAL, CONF_DEVICE_CLASS

_LOGGER = logging.getLogger(__name__)

CONF_ENABLED_INPUTS = 'enabled_inputs'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
  {
    vol.Optional(CONF_ENABLED_INPUTS): list,
    vol.Optional(CONF_SCAN_INTERVAL, default=timedelta(seconds=5)): cv.time_period,
    vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
  }
)

def setup_platform(hass, config, add_devices, discovery_info=None):
  """Setup the IPX800 Sensor platform."""

  _LOGGER.debug("Entering binary_sensor.setup_platform")
  # Assign configuration variables. 
  enabled_inputs = config.get(CONF_ENABLED_INPUTS)
  scan_interval = config.get(CONF_SCAN_INTERVAL).total_seconds()
  device_class = config.get(CONF_DEVICE_CLASS)
  
  ipxdata = hass.data[DOMAIN]
  if ipxdata.update() == None:
    _LOGGER.warning("update failed")
    return 

  if enabled_inputs != None and len(enabled_inputs) > 0:
    # Instanciate IPXInputs
    inputs = []
    for r in enabled_inputs:
      if ipxdata.inputs!=None and len(ipxdata.inputs)>=r :
        inputs.append(ipxdata.inputs[r-1])
      else:
        _LOGGER.warning("Requested inputs %i does not exists", r)
        
    # Add IPX800Sensor devices
    if (inputs):
      add_devices(IPX800BinarySensor(input, device_class) for input in inputs)



class IPX800BinarySensor(BinarySensorDevice):
  """Representation of a binary sensor as input of IPX """

  def __init__(self, obj, device_class):
    """Initialize an IPX800BinarySensor."""
    self._obj = obj
    self._device_class = device_class
    self._updatets = time.time()
    self._state = None

  @property
  def name(self):
    """Return the display name of this sensor."""
    return self._obj.name

  @property
  def is_on(self):
    """Return true if input is on."""
    return self._state

  @property
  def should_poll(self):
    """Return the polling state."""
    return True
    
  @property
  def device_class(self):
      """Return the sensor class of the sensor."""
      return self._device_class

  def update(self):
    """Fetch new state data for this input.
    This is the only method that should fetch new data for Home Assistant.    """
    # Only update every update_interval
    self._state = self._obj.state
