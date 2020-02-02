# -*- coding: utf-8 *-*

import sys
import logging
import time
from datetime import timedelta
from threading import Lock
from . import DOMAIN
import voluptuous as vol

# Import the device class from the component that you want to support
from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity
from homeassistant.const import CONF_SCAN_INTERVAL, CONF_DEVICE_CLASS

_LOGGER = logging.getLogger(__name__)

CONF_ENABLED_COUNTERS = 'enabled_counters'
CONF_ENABLED_ANALOGS = 'enabled_analogs'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
  {
    vol.Optional(CONF_ENABLED_COUNTERS): list,
    vol.Optional(CONF_ENABLED_ANALOGS): list,
    vol.Optional(CONF_SCAN_INTERVAL, default=timedelta(seconds=5)): cv.time_period
  }
)

def setup_platform(hass, config, add_devices, discovery_info=None):
  """Setup the IPX800 Sensor platform."""

  _LOGGER.debug("Entering sensor.setup_platform")
  # Assign configuration variables. 
  enabled_counters = config.get(CONF_ENABLED_COUNTERS)
  enabled_analogs = config.get(CONF_ENABLED_ANALOGS)
  scan_interval = config.get(CONF_SCAN_INTERVAL).total_seconds()
  device_class = config.get(CONF_DEVICE_CLASS)

  ipxdata = hass.data[DOMAIN]
  if ipxdata.update() == None:
    _LOGGER.warning("update failed")
    return 
  
  if enabled_counters != None and len(enabled_counters) > 0:
    # Instanciate IPXCounters
    counters = []
    for r in enabled_counters:
      if ipxdata.counters!=None and len(ipxdata.counters)>=r :
        ipxdata.counters[r-1].setscaninterval(scan_interval)
        counters.append(ipxdata.counters[r-1])
      else:
        _LOGGER.warning("Requested counters %i does not exists", r)
        
    # Add IPX800Sensor devices
    if (counters):
      add_devices(IPX800Sensor(counter, device_class) for counter in counters)

  if enabled_analogs != None and len(enabled_analogs) > 0:
    # Instanciate IPXAnalogs
    analogs = []
    for r in enabled_analogs:
      if ipxdata.analogs!=None and len(ipxdata.analogs)>=r :
        analogs.append(ipxdata.analogs[r-1])
      else:
        _LOGGER.warning("Requested analog %i does not exists", r)

    # Add IPX800Sensor devices
    if (analogs):
      add_devices(IPX800Sensor(analog, device_class) for analog in analogs)


class IPX800Sensor(Entity):
  """Representation of a sensor connected to IPX """

  def __init__(self, obj, device_class):
    """Initialize an IPX800Sensor."""
    self._obj = obj
    self._device_class = device_class
    self._state = None
    
  @property
  def name(self):
    """Return the display name of this sensor."""
    return self._obj.name

  @property
  def state(self):
    """Return the value of the counter."""
    return str(self._state)

  @property
  def should_poll(self):
    """Return the polling state."""
    return True

  @property
  def device_class(self):
      """Return the sensor class of the sensor."""
      return self._device_class

  def update(self):
    """Fetch new state data for this light.
    This is the only method that should fetch new data for Home Assistant.    """
    # Only update every update_interval
    self._state = self._obj.state


