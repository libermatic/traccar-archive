# traccar-archive

Use `pt-archiver` to archive `tc_positions` and `tc_events` rows past a given date.

## Environment variables

- `DAYS_PAST`: number of before before which data will be archived. Default `180`.
- `DSN_CONF`: path of the _mysql_ creds
- `GCS_CONF`: path of the _Google Cloud Storage_ config
- `GOOGLE_APPLICATION_CREDENTIALS`: path of the _Google_ service account creds
- `DEBUG`: set to `True` to enable logging

## Files

- _mysql_ creds
```json
{
    "host": "host",
    "database": "database",
    "user": "user",
    "password": "password"
}
```

- _Google Cloud Storage_ config
```json
{
    "bucket": "bucket"
}
```

- _Google_ service account creds.
https://cloud.google.com/storage/docs/reference/libraries#setting_up_authentication


