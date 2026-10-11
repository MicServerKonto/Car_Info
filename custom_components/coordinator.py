"""Data update coordinator for Car Info."""
from __future__ import annotations

import logging
from datetime import timedelta
import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, API_BASE_URL, API_AUTH_HEADER

_LOGGER = logging.getLogger(__name__)


class CarInfoCoordinator(DataUpdateCoordinator[dict]):
    """Coordinator to manage fetching Car Info data from MotorAPI."""

    def __init__(self, hass: HomeAssistant, api_key: str, registration_number: str) -> None:
        """Initialize coordinator."""
        self.api_key = api_key
        self.registration_number = registration_number.upper()
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(hours=12),
        )

    async def _async_update_data(self) -> dict:
        """Fetch data from MotorAPI."""
        url = f"{API_BASE_URL}/vehicles/{self.registration_number}"
        headers = {
            API_AUTH_HEADER: self.api_key,
            "Accept": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as response:
                    if response.status == 401:
                        raise UpdateFailed("Invalid API key")
                    if response.status == 404:
                        raise UpdateFailed(f"Vehicle {self.registration_number} not found")
                    if response.status != 200:
                        raise UpdateFailed(f"Error fetching data: HTTP {response.status}")
                    
                    return await response.json()
            except aiohttp.ClientError as error:
                raise UpdateFailed(f"Communication error: {error}") from error