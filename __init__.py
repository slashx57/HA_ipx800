# -*- coding: utf-8 *-*

import sys
import logging
import voluptuous as vol
from threading import Lock

# Import the device class from the component that you want to support
from homeassistant.const import CONF_HOST, CONF_API_KEY, CONF_PORT, CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.discovery import load_platform

from pyipx800.pyipx800 import pyipx800
from pyipx800.pyipxInput import Input
from pyipx800.pyipxRelay import Relay
from pyipx800.pyipxAnalog import Analog
from pyipx800.pyipxCounter import  Counter
from pyipx800.pyipxVirtuals import VirtualInput, VirtualOutput, VirtualAnalog

DOMAIN = "ipx800"
DEFAULT_PORT = 80

# Home Assistant depends on 3rd party packages for API specific code.
REQUIREMENTS = ['requests', 'requests-xml']

_LOGGER = logging.getLogger(__name__)

# Schema to validate the user's configuration
CONFIG_SCHEMA = vol.Schema({
  DOMAIN: vol.Schema({
    vol.Required(CONF_HOST): cv.string,
    vol.Optional(CONF_PORT, default=DEFAULT_PORT): cv.port,
    vol.Required(CONF_API_KEY): cv.string,
    vol.Optional(CONF_USERNAME): cv.string,
    vol.Optional(CONF_PASSWORD): cv.string
  })
},extra=vol.ALLOW_EXTRA)

def setup(hass, config):
  """Set up is called when Home Assistant is loading our component."""
  #from pyipx800 import pyipx800
  
  _LOGGER.debug("Entering setup")
  
  # Assign configuration variables. The configuration check takes care they are
  # present.
  conf = config[DOMAIN]
  host = conf.get(CONF_HOST)
  port = conf.get(CONF_PORT)
  apikey = conf.get(CONF_API_KEY)
  username = conf.get(CONF_USERNAME)
  password = conf.get(CONF_PASSWORD)

  hass.data[DOMAIN] = IpxData(host, port, apikey)
  try:
    hass.data[DOMAIN].update()
  except:
    _LOGGER.error("Update error %s", str(sys.exc_info()[0]))
    return False
    
  #load_platform(hass, 'sensor', DOMAIN, {}, config)
  #load_platform(hass, 'light', DOMAIN, {}, config)

  _LOGGER.debug("Exiting setup")

  # Return boolean to indicate that initialization was successfully.
  return True

class IpxData:
  """Stores the data """
  
  def __init__(self, host, port, apikey):
    self.mutex = Lock()
    self._ipx = None
    self._host = host
    self._port = port
    self._apikey = apikey
    self.inputs = None
    self.relays = None
    self.analogs = None
    self.counters = None
    self.virt_inputs = None
    self.virt_outputs = None
    self.virt_analogs = None
    
  def update(self):
    with self.mutex:
      if self._ipx == None:
        # Setup connection with IPX800
        self._ipx = pyipx800(self._host, self._port, self._apikey)
        self._ipx.configure()
        
        self.counters = self._ipx.counters
        _LOGGER.debug("counters found:"+str(len(self.counters)))
        
        self.relays = self._ipx.relays
        _LOGGER.debug("relays found:"+str(len(self.relays)))
        
        self.analogs = self._ipx.analogs
        _LOGGER.debug("analogs found:"+str(len(self.analogs)))
      
        self.inputs = self._ipx.inputs
        _LOGGER.debug("inputs found:"+str(len(self.inputs)))
        
        self.virt_inputs = self._ipx.virt_inputs
        _LOGGER.debug("virt_inputs found:"+str(len(self.virt_inputs)))
        
        self.virt_outputs = self._ipx.virt_outputs
        _LOGGER.debug("virt_outputs found:"+str(len(self.virt_outputs)))
        
        self.virt_analogs = self._ipx.virt_analogs
        _LOGGER.debug("virt_analogs found:"+str(len(self.virt_analogs)))
        
    return self._ipx
