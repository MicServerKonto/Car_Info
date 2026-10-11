"""The Car Info integration."""
from __future__ import annotations

import logging
import aiohttp
import voluptuous as vol

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall, ServiceResponse, SupportsResponse
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv

from .const import (
    API_AUTH_HEADER,
    API_BASE_URL,
    CONF_API_KEY,
    CONF_REGISTRATION,
    DOMAIN,
    SERVICE_LOOKUP_VEHICLE,
)
from .coordinator import CarInfoCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR, Platform.CALENDAR]

LOOKUP_VEHICLE_SCHEMA = vol.Schema(
    {
        vol.Required("registration_number"): cv.string,
    }
)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Car Info from a config entry."""
    coordinator = CarInfoCoordinator(
        hass,
        entry.data[CONF_API_KEY],
        entry.data[CONF_REGISTRATION],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def async_handle_lookup_vehicle(call: ServiceCall) -> ServiceResponse:
        """Handle the lookup_vehicle service call and return data."""
        registration_number = call.data["registration_number"].upper()
        api_key = entry.data[CONF_API_KEY]

        url = f"{API_BASE_URL}/vehicles/{registration_number}"
        headers = {
            API_AUTH_HEADER: api_key,
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 404:
                        raise HomeAssistantError(f"Køretøj {registration_number} blev ikke fundet.")
                    if response.status == 401:
                        raise HomeAssistantError("Ugyldig API-nøgle.")
                    if response.status != 200:
                        raise HomeAssistantError(
                            f"Fejl ved opslag på {registration_number}: HTTP {response.status}"
                        )
                    return await response.json()
            except aiohttp.ClientError as err:
                raise HomeAssistantError(f"Kommunikationsfejl med MotorAPI: {err}") from err

    # Register service/action matching services.yaml
    hass.services.async_register(
        DOMAIN,
        SERVICE_LOOKUP_VEHICLE,
        async_handle_lookup_vehicle,
        schema=LOOKUP_VEHICLE_SCHEMA,
        supports_response=SupportsResponse.ONLY,
    )

    # Automatic reload on options update
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))

    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Handle options update by reloading the entry."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(entry, PLATFORMS):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok