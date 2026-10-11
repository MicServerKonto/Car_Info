"""Constants for the Car Info integration."""
from __future__ import annotations

DOMAIN = "car_info"

API_BASE_URL = "https://v1.motorapi.dk"
API_AUTH_HEADER = "X-AUTH-TOKEN"

CONF_API_KEY = "api_key"
CONF_REGISTRATION = "registration_number"
CONF_REGISTRATION_NUMBER = "registration_number"

CONF_SHOW_INSPECT = "show_inspect"
CONF_SHOW_INSPECTION = "show_inspection"
CONF_SHOW_LEASING = "show_leasing"
CONF_SHOW_STATUS = "show_status"
CONF_SHOW_VEHICLE = "show_vehicle"
CONF_SHOW_WEIGHT = "show_weight"
CONF_SHOW_ENGINE = "show_engine"

SERVICE_LOOKUP_VEHICLE = "lookup_vehicle"

# Field constants used for calendar
FIELD_MAKE = "make"
FIELD_MODEL = "model"
FIELD_MOT_INFO = "mot_info"
FIELD_MOT_DATE = "date"
FIELD_NEXT_INSPECTION = "next_inspection_date"