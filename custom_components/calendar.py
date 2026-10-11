"""Calendar events for last and next vehicle inspections."""
from __future__ import annotations

import logging
from datetime import date, datetime, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.util import dt as dt_util
from .const import (
    DOMAIN,
    FIELD_MAKE,
    FIELD_MODEL,
    FIELD_MOT_INFO,
    FIELD_MOT_DATE,
    FIELD_NEXT_INSPECTION,
    CONF_SHOW_INSPECT,
)
from .coordinator import CarInfoCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Car Info calendar based on config/options entries."""
    coordinator: CarInfoCoordinator = hass.data[DOMAIN][entry.entry_id]

    show_inspect = entry.options.get(
        CONF_SHOW_INSPECT, entry.data.get(CONF_SHOW_INSPECT, True)
    )

    if show_inspect:
        async_add_entities([CarInfoCalendar(coordinator, entry)])


class CarInfoCalendar(CoordinatorEntity[CarInfoCoordinator], CalendarEntity):
    """Representation of a Car Info calendar entity."""

    _attr_has_entity_name = True
    _attr_name = "inspect"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        """Initialize the calendar entity."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_inspect"

    @property
    def device_info(self) -> DeviceInfo:
        """Return device information."""
        data = self.coordinator.data or {}
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.registration_number)},
            name=self.coordinator.registration_number,
            manufacturer=data.get(FIELD_MAKE) or "Unknown",
            model=data.get(FIELD_MODEL) or None,
        )

    def _events(self) -> list[CalendarEvent]:
        data = self.coordinator.data or {}
        mot = data.get(FIELD_MOT_INFO) or {}
        description = (
            f"{data.get(FIELD_MAKE, '')} {data.get(FIELD_MODEL, '')}".strip()
            or self.coordinator.registration_number
        )
        events = []
        for key, label in (
            (FIELD_NEXT_INSPECTION, "inspect"),
            (FIELD_MOT_DATE, "last inspection"),
        ):
            raw = mot.get(key)
            if not raw:
                continue
            try:
                event_date = date.fromisoformat(str(raw)[:10])
            except (ValueError, TypeError):
                _LOGGER.debug("Unable to parse inspection date %s", raw)
                continue
            events.append(
                CalendarEvent(
                    start=event_date,
                    end=event_date + timedelta(days=1),
                    summary=f"{label} - {self.coordinator.registration_number}",
                    description=description,
                )
            )
        return events

    @property
    def event(self) -> CalendarEvent | None:
        """Return the next upcoming event."""
        today = dt_util.now().date()
        upcoming = [event for event in self._events() if event.end >= today]
        return min(upcoming, key=lambda event: event.start) if upcoming else None

    async def async_get_events(
        self, hass: HomeAssistant, start_date: datetime, end_date: datetime
    ) -> list[CalendarEvent]:
        """Return calendar events within a datetime range."""
        start = start_date.date() if isinstance(start_date, datetime) else start_date
        end = end_date.date() if isinstance(end_date, datetime) else end_date
        return [
            event
            for event in self._events()
            if event.start <= end and event.end >= start
        ]