# Car_Info
## Known Limitations

- Data availability depends on MotorAPI from the danish motorregister
- if the vehicle is not registered in the danish motorregister, then no data is returned
- Inspection date is the scheduled deadline, not a confirmed appointment

## Requirements

| Requirement | Get API |
|---|---|
| MotorAPI API key | Free — apply at [www.motorapi.dk](https://www.motorapi.dk) |

  ## Rate limits

- The free Motor API tier has a daily request quota. The integration returns a clear error if the quota is exceeded.
- You can check your usage at `https://v1.motorapi.dk/usage` (or via the Motor API dashboard).

## Features

- **Grouped Sensors**: Organized into logical sensors (Vehicle, Status, Leasing, Weight, Engine, and Inspection) that can be toggled on or off via the configuration options.
- **Inspection Calendar**: Calendar entity (`<registration_number> inspect`) displaying events for both next inspection and last inspection, fully integrated with the Home Assistant Calendar dashboard and automations.
- **Custom Action (`lookup_vehicle`)**: Built-in action to perform on-demand vehicle lookups via MotorAPI with full response data support (`vehicle_data`).
- **Dynamic Options Reload**: Configuration changes (toggling sensors or calendar) apply instantly without requiring an integration restart.
- **Multi-Vehicle Support**: Add multiple vehicles seamlessly with one config entry per registration number.
- **Official Source**: Data fetched via [MotorAPI](https://www.motorapi.dk), querying the official Danish Motor Register (Motorregistret).

---

## Configuration

1. Go to **Settings → Devices & Services → Add Integration**.
2. Search for **Car Info**.
3. Enter the required fields:

| Field | Description |
|---|---|
| API key | Your MotorAPI key from motorapi.dk |
| Registration number | Vehicle license plate (e.g. `AB12345`) |

Post-setup options are available via **Configure** on the integration card:

| Option | Description | Default |
|---|---|---|
| Engine | Enable odometer sensor | Off |
| Inspect | Enable chassis number sensor | Off |
| inspection | Enable vehicle make sensor | Off |
| Leasing | Enable vehicle model sensor | Off |
| Status | Enable model year sensor | Off |
| Vehicle | Enable vehicle use type sensor | On |
| Weight | Enable vehicle use type sensor | Off |

## Data

### Sensors

| Sensor | Attributes |
|---|---|
| `Engine` | engine_volume: engine_cylinders: fuel_type: is_hybrid: hybrid_type: |
| `Inspect` | message: all_day: start_time: end_time: location: description: |
| `inspection` | days_until_next_inspection: last_inspection_date: mileage_at_last_inspection: mot_info_result: mot_info_status: mot_info_status_date: mot_info_type: |
| `Leasing` | leasing_from: leasing_to: |
| `Status` | status_date: first_registration: registration_zipcode: |
| `Vehicle` | model: variant: model_year: model_type: color: type: vehicle_use: vehicle_id: vin: chassis_type: registration_number: description: axels: pulling_axels: doors: seats: |
| `Weight` | cerb_weight: own_weight: coupling: trailer_maxweight_nobrakes: trailer_maxweight_withbrakes: |


### Update interval

Data is fetched every 24 hours.

### Actions

Perform a vehicle_lookups with full response data of vehicle.

```yaml
action: car_info.lookup_vehicle
data:
  registration_number: xx12345
