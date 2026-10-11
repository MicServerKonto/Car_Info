"""Config flow for Car Info integration."""
from __future__ import annotations

from typing import Any
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback

DOMAIN = "car_info"


class CarInfoConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Car Info."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            sensor_keys = [
                "show_inspect",
                "show_inspection",
                "show_leasing",
                "show_status",
                "show_vehicle",
                "show_weight",
                "show_engine",
            ]
            if not any(user_input.get(key, False) for key in sensor_keys):
                errors["base"] = "no_sensors_selected"
            else:
                await self.async_set_unique_id(user_input["registration_number"].upper())
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=user_input["registration_number"].upper(),
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required("api_key"): str,
                    vol.Required("registration_number"): str,
                    vol.Optional("show_inspect", default=False): bool,
                    vol.Optional("show_inspection", default=False): bool,
                    vol.Optional("show_leasing", default=False): bool,
                    vol.Optional("show_status", default=False): bool,
                    vol.Optional("show_vehicle", default=True): bool,
                    vol.Optional("show_weight", default=False): bool,
                    vol.Optional("show_engine", default=False): bool,
                }
            ),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> CarInfoOptionsFlowHandler:
        """Get the options flow for this handler."""
        return CarInfoOptionsFlowHandler()


class CarInfoOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle options flow for Car Info."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(
                        "show_inspect",
                        default=self.config_entry.options.get(
                            "show_inspect",
                            self.config_entry.data.get("show_inspect", False),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_inspection",
                        default=self.config_entry.options.get(
                            "show_inspection",
                            self.config_entry.data.get("show_inspection", True),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_leasing",
                        default=self.config_entry.options.get(
                            "show_leasing",
                            self.config_entry.data.get("show_leasing", False),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_status",
                        default=self.config_entry.options.get(
                            "show_status",
                            self.config_entry.data.get("show_status", True),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_vehicle",
                        default=self.config_entry.options.get(
                            "show_vehicle",
                            self.config_entry.data.get("show_vehicle", True),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_weight",
                        default=self.config_entry.options.get(
                            "show_weight",
                            self.config_entry.data.get("show_weight", False),
                        ),
                    ): bool,
                    vol.Optional(
                        "show_engine",
                        default=self.config_entry.options.get(
                            "show_engine",
                            self.config_entry.data.get("show_engine", True),
                        ),
                    ): bool,
                }
            ),
        )