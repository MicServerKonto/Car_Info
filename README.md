# Car_Info
## Known Limitations

- Data availability depends on MotorAPI from the danish motorregister
- if the vehicle is not registered in the danish motorregister, then no data is returned
- Inspection date is the scheduled deadline, not a confirmed appointment

## Requirements

| Requirement | Get API |
|---|---|
| MotorAPI API key | Free — apply at [www.motorapi.dk](https://www.motorapi.dk) |

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
| Mileage at last inspection | Enable odometer sensor | Off |
| VIN | Enable chassis number sensor | Off |
| Make | Enable vehicle make sensor | Off |
| Model | Enable vehicle model sensor | Off |
| Model year | Enable model year sensor | Off |
| Vehicle use | Enable vehicle use type sensor | Off |

## Data

### Sensors

| Sensor | Always shown | Type | Attributes |
|---|---|---|---|
| `Engine` | Yes | `int` | engine_volume: engine_cylinders: fuel_type: is_hybrid: hybrid_type: |
| `Inspect` | Yes | `string` | message: all_day: start_time: end_time: location: description: |
| `inspection` | Yes | `string` | days_until_next_inspection: last_inspection_date: mileage_at_last_inspection: mot_info_result: mot_info_status: mot_info_status_date: mot_info_type: |
| `Leasing` | Yes | `string` | leasing_from: null leasing_to: |
| `Status` | Optional | `int` | status_date: first_registration: registration_zipcode: |
| `Vehicle` | Optional | `string` | model: variant: model_year: model_type: color: type: vehicle_use: vehicle_id: vin: chassis_type: registration_number: description: axels: pulling_axels: doors: seats: |
| `Weight` | Optional | `string` | cerb_weight: own_weight: coupling: trailer_maxweight_nobrakes: trailer_maxweight_withbrakes: |


### Update interval

Data is fetched every 24 hours.
