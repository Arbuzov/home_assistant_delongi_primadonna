import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import AVAILABLE_PROFILES, DOMAIN
from .device import DelonghiDeviceEntity, DelongiPrimadonna

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
        hass: HomeAssistant, entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback):
    delongh_device: DelongiPrimadonna = hass.data[DOMAIN][entry.unique_id]
    async_add_entities([
        ProfileSelect(delongh_device, hass)
    ])
    return True


class ProfileSelect(DelonghiDeviceEntity, SelectEntity):
    """A select implementation for profile selection."""

    _attr_name = 'Profile'
    _attr_options = list(AVAILABLE_PROFILES.keys())
    _attr_current_option = list(AVAILABLE_PROFILES.keys())[0]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        profile_id = AVAILABLE_PROFILES.get(option)
        self.hass.async_create_task(self.device.select_profile(profile_id))
        self._attr_current_option = option