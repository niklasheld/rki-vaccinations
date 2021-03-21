"""The COVID-19 Vaccinations Germany integration."""
import asyncio

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import asyncio
from datetime import timedelta
import logging

import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers import aiohttp_client, update_coordinator

from .vaccination_api import get_vaccination_stats

from .const import DOMAIN

PLATFORMS = ["sensor"]


async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the COVID-19 Vaccinations Germany component."""
    await get_coordinator(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up COVID-19 Vaccinations Germany from a config entry."""

    for platform in PLATFORMS:
        hass.async_create_task(
            hass.config_entries.async_forward_entry_setup(entry, platform)
        )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )

    return unload_ok


async def get_coordinator(hass):
    """Get the data update coordinator."""
    if DOMAIN in hass.data:
        return hass.data[DOMAIN]

    async def async_get_cases():
        with async_timeout.timeout(10):
            return await get_vaccination_stats(
                aiohttp_client.async_get_clientsession(hass)
            )

    hass.data[DOMAIN] = update_coordinator.DataUpdateCoordinator(
        hass,
        logging.getLogger(__name__),
        name=DOMAIN,
        update_method=async_get_cases,
        update_interval=timedelta(hours=4),
    )
    await hass.data[DOMAIN].async_refresh()
    return hass.data[DOMAIN]
