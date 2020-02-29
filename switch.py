# -*- coding: utf-8 *-*

import logging

import voluptuous as vol
from . import DOMAIN

# Import the device class from the component that you want to support
from homeassistant.components.switch import PLATFORM_SCHEMA, SwitchDevice
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

CONF_ENABLED_RELAYS = 'enabled_relays'
CONF_ENABLED_INPUTS = 'enabled_virtualinputs'
CONF_ENABLED_OUTPUTS = 'enabled_virtualoutputs'

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
  vol.Optional(CONF_ENABLED_RELAYS): list,
  vol.Optional(CONF_ENABLED_INPUTS): list,
  vol.Optional(CONF_ENABLED_OUTPUTS): list,
})


def setup_platform(hass, config, add_devices, discovery_info=None):
  """Setup the IPX800 Light platform."""

  _LOGGER.debug("Entering switch.setup_platform")
  # Assign configuration variables. 
  enabled_relays = config.get(CONF_ENABLED_RELAYS)
  enabled_inputs = config.get(CONF_ENABLED_INPUTS)
  enabled_outputs = config.get(CONF_ENABLED_OUTPUTS)

  ipxdata = hass.data[DOMAIN]
  if ipxdata.update() == None:
    _LOGGER.warning("update failed")
    return 

  if enabled_relays != None and len(enabled_relays) > 0:
    # Instanciate IPXRelays
    relays = []
    for r in enabled_relays:
      if ipxdata.relays!=None and len(ipxdata.relays)>=r :
        relays.append(ipxdata.relays[r-1])
      else:
        _LOGGER.warning(r)
        _LOGGER.warning(ipxdata.relays)
        _LOGGER.warning("Requested relay %i does not exists", r)
    # Add IPX800Switch devices
    add_devices(IPX800Switch(relay) for relay in relays)

  if enabled_inputs != None and len(enabled_inputs) > 0:
    # Instanciate VirtualInput
    virt_inputs = []
    for r in enabled_inputs:
      if ipxdata.virt_inputs!=None and len(ipxdata.virt_inputs)>=r :
        virt_inputs.append(ipxdata.virt_inputs[r-1])
      else:
        _LOGGER.warning(r)
        _LOGGER.warning(ipxdata.virt_inputs)
        _LOGGER.warning("Requested input %i does not exists", r)
    # Add IPX800Switch devices
    add_devices(IPX800Switch(input) for input in virt_inputs)

  if enabled_outputs != None and len(enabled_outputs) > 0:
    # Instanciate IPXRelays
    virt_outputs = []
    for r in enabled_outputs:
      if ipxdata.virt_outputs!=None and len(ipxdata.virt_outputs)>=r :
        virt_outputs.append(ipxdata.virt_outputs[r-1])
      else:
        _LOGGER.warning(r)
        _LOGGER.warning(ipxdata.virt_outputs)
        _LOGGER.warning("Requested output %i does not exists", r)
    # Add IPX800Switch devices
    add_devices(IPX800Switch(output) for output in virt_outputs)

class IPX800Switch(SwitchDevice):
  """Representation of a switch for IPX"""

  def __init__(self, obj):
    """Initialize an IPX800Switch."""
    self._obj = obj
    self._state = False
    _LOGGER.debug(f"[switch.{obj.name}] added")

  @property
  def name(self):
    """Return the display name of this switch."""
    return self._obj.name

  @property
  def is_on(self):
    """Return true if switch is on."""
    return self._state

  def turn_on(self, **kwargs):
    """Instruct the switch to turn on.
    """
    self._obj.on()

  def turn_off(self, **kwargs):
    """Instruct the switch to turn off."""
    self._obj.off()

  def update(self):
    """Fetch new state data for this switch.

    This is the only method that should fetch new data for Home Assistant.
    """
    self._state = self._obj.state


  

