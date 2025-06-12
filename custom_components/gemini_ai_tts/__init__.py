"""Gemini AI TTS/STT Integration for Home Assistant."""
from __future__ import annotations

import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.TTS,
    Platform.STT,
    Platform.CONVERSATION,
]


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up the Gemini AI TTS/STT integration."""
    hass.data.setdefault(DOMAIN, {})
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Gemini AI TTS/STT from a config entry."""
    try:
        hass.data.setdefault(DOMAIN, {})
        hass.data[DOMAIN][entry.entry_id] = entry.data

        await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
        
        # Set up services
        from .services import async_setup_services
        await async_setup_services(hass)
        
        # Reload entry when options are updated
        entry.async_on_unload(entry.add_update_listener(async_reload_entry))
        
        _LOGGER.info("Successfully set up Gemini AI TTS/STT integration")
        return True
        
    except Exception as err:
        _LOGGER.error("Error setting up Gemini AI TTS/STT integration: %s", err, exc_info=True)
        return False


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    try:
        if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
            hass.data[DOMAIN].pop(entry.entry_id, None)
        
        _LOGGER.info("Successfully unloaded Gemini AI TTS/STT integration")
        return unload_ok
        
    except Exception as err:
        _LOGGER.error("Error unloading Gemini AI TTS/STT integration: %s", err, exc_info=True)
        return False


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Reload config entry."""
    try:
        await async_unload_entry(hass, entry)
        await async_setup_entry(hass, entry)
        _LOGGER.info("Successfully reloaded Gemini AI TTS/STT integration")
    except Exception as err:
        _LOGGER.error("Error reloading Gemini AI TTS/STT integration: %s", err, exc_info=True)
