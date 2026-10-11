"""Support for Car Info grouped sensors."""
from __future__ import annotations

import json
from datetime import date
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import dt as dt_util

from .const import (
    DOMAIN,
    CONF_SHOW_INSPECTION,
    CONF_SHOW_LEASING,
    CONF_SHOW_STATUS,
    CONF_SHOW_VEHICLE,
    CONF_SHOW_WEIGHT,
    CONF_SHOW_ENGINE,
)
from .coordinator import CarInfoCoordinator


def _flatten(data: dict[str, Any], prefix: str = "") -> dict[str, Any]:
    """Flatten nested dictionaries and make keys lowercase for robust matching."""
    result: dict[str, Any] = {}
    for key, value in data.items():
        clean_key = str(key).lower()
        path = f"{prefix}_{clean_key}" if prefix else clean_key
        
        if isinstance(value, dict):
            result.update(_flatten(value, path))
        elif isinstance(value, (list, tuple)):
            result[path] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        elif value is None or isinstance(value, (str, int, float, bool)):
            result[path] = value
        else:
            result[path] = str(value)
    return result


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Car Info sensors based on config/options entries."""
    coordinator: CarInfoCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[CarInfoSensorBase] = []

    def is_enabled(option_key: str, default: bool = False) -> bool:
        return entry.options.get(option_key, entry.data.get(option_key, default))

    if is_enabled(CONF_SHOW_VEHICLE, True):
        entities.append(CarInfoVehicleSensor(coordinator, entry))
    if is_enabled(CONF_SHOW_STATUS, True):
        entities.append(CarInfoStatusSensor(coordinator, entry))
    if is_enabled(CONF_SHOW_LEASING, False):
        entities.append(CarInfoLeasingSensor(coordinator, entry))
    if is_enabled(CONF_SHOW_WEIGHT, False):
        entities.append(CarInfoWeightSensor(coordinator, entry))
    if is_enabled(CONF_SHOW_ENGINE, True):
        entities.append(CarInfoEngineSensor(coordinator, entry))
    if is_enabled(CONF_SHOW_INSPECTION, True):
        entities.append(CarInfoInspectionSensor(coordinator, entry))

    async_add_entities(entities)


class CarInfoSensorBase(CoordinatorEntity[CarInfoCoordinator], SensorEntity):
    """Base class for Car Info grouped sensors."""

    _attr_has_entity_name = True

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator)
        self.entry_id = entry.entry_id

    @property
    def device_info(self) -> DeviceInfo:
        data = _flatten(self.coordinator.data or {})
        return DeviceInfo(
            identifiers={(DOMAIN, self.coordinator.registration_number)},
            name=f"Car Info {self.coordinator.registration_number}",
            manufacturer=str(data.get("make") or "Unknown"),
            model=str(data.get("model") or "") or None,
        )


class CarInfoVehicleSensor(CarInfoSensorBase):
    """Sensor representing general vehicle information."""

    _attr_name = "Vehicle"
    _attr_icon = "mdi:car"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_vehicle"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("make")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        return {
            "model": data.get("model"),
            "variant": data.get("variant"),
            "model_year": data.get("model_year"),
            "model_type": data.get("model_type"),
            "color": data.get("color"),
            "type": data.get("type"),
            "vehicle_use": data.get("use"),
            "vehicle_id": data.get("vehicle_id"),
            "vin": data.get("vin"),
            "chassis_type": data.get("chassis_type"),
            "registration_number": data.get("registration_number"),
            "description": data.get("description") or f"{data.get('make', '')} {data.get('model', '')}".strip(),
            "axels": data.get("axels"),
            "pulling_axels": data.get("pulling_axels"),
            "doors": data.get("doors"),
            "seats": data.get("seats"),
        }


class CarInfoStatusSensor(CarInfoSensorBase):
    """Sensor representing registration and vehicle status."""

    _attr_name = "Status"
    _attr_icon = "mdi:shield-check"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_status"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("status")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        return {
            "status_date": data.get("status_date"),
            "first_registration": data.get("first_registration"),
            "registration_zipcode": data.get("registration_zipcode"),
        }


class CarInfoLeasingSensor(CarInfoSensorBase):
    """Sensor representing leasing details."""

    _attr_name = "Leasing"
    _attr_icon = "mdi:file-document-outline"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_leasing"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("is_leasing")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        return {
            "leasing_from": data.get("leasing_from"),
            "leasing_to": data.get("leasing_to"),
        }


class CarInfoWeightSensor(CarInfoSensorBase):
    """Sensor representing weights and dimensions."""

    _attr_name = "Weight"
    _attr_icon = "mdi:weight"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_weight"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("total_weight")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        return {
            "cerb_weight": data.get("cerb_weight"),
            "own_weight": data.get("own_weight"),
            "coupling": data.get("coupling"),
            "trailer_maxweight_nobrakes": data.get("trailer_maxweight_nobrakes"),
            "trailer_maxweight_withbrakes": data.get("trailer_maxweight_withbrakes"),
        }


class CarInfoEngineSensor(CarInfoSensorBase):
    """Sensor representing engine and powertrain details."""

    _attr_name = "Engine"
    _attr_icon = "mdi:engine"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_engine"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("engine_power")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        return {
            "engine_volume": data.get("engine_volume"),
            "engine_cylinders": data.get("engine_cylinders"),
            "fuel_type": data.get("fuel_type"),
            "is_hybrid": data.get("is_hybrid"),
            "hybrid_type": data.get("hybrid_type"),
        }


class CarInfoInspectionSensor(CarInfoSensorBase):
    """Sensor representing inspection and MOT info."""

    _attr_name = "Inspection"
    _attr_icon = "mdi:calendar-clock"

    def __init__(self, coordinator: CarInfoCoordinator, entry: ConfigEntry) -> None:
        super().__init__(coordinator, entry)
        self._attr_unique_id = f"{entry.entry_id}_inspection"

    @property
    def native_value(self) -> Any:
        data = _flatten(self.coordinator.data or {})
        return data.get("mot_info_next_inspection_date")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        data = _flatten(self.coordinator.data or {})
        raw_date = data.get("mot_info_next_inspection_date")
        days_until = None
        if raw_date:
            try:
                days_until = (date.fromisoformat(str(raw_date)[:10]) - dt_util.now().date()).days
            except (TypeError, ValueError):
                pass
        return {
            "days_until_next_inspection": days_until,
            "last_inspection_date": data.get("mot_info_date"),
            "mileage_at_last_inspection": data.get("mot_info_mileage"),
            "mot_info_result": data.get("mot_info_result"),
            "mot_info_status": data.get("mot_info_status"),
            "mot_info_status_date": data.get("mot_info_status_date"),
            "mot_info_type": data.get("mot_info_type"),
        }