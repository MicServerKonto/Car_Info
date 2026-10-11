# Car_Info
## Known Limitations

- Data availability depends on MotorAPI from the danish motorregister
- if the vehicle is not registered in the danish motorregister, then no data is returned
- Inspection date is the scheduled deadline, not a confirmed appointment

## Requirements

| Requirement | Version / Details |
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

---
