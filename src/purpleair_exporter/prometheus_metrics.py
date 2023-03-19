from prometheus_client import Gauge, Info
from prometheus_client import REGISTRY

registry = REGISTRY

purpleair_temp_gauge = Gauge('purpleair_temp', 'PurpleAir air quality sesnor temperature reading in fahrenheit', ["sensor_host", "sensor_id"])  # current_temp_f
purpleair_humidity_gauge = Gauge('purpleair_humidity', 'PurpleAir air quality sesnor humidity reading', ["sensor_host", "sensor_id"])  # current_humidity
purpleair_dewpoint_gauge = Gauge('purpleair_dewpoint', 'PurpleAir air quality sesnor dewpoint reading in fahrenheit', ["sensor_host", "sensor_id"])  # current_dewpoint_f
purpleair_pressure_gauge = Gauge('purpleair_pressure', 'PurpleAir air quality sesnor pressure reading', ["sensor_host", "sensor_id"])  # pressure
purpleair_pm25aqi_gauge = Gauge('purpleair_pm25aqi', 'PurpleAir air quality sesnor PM2.5 AQI reading', ["sensor_host", "sensor_id"])  # pm2.5_aqi
purpleair_httpsuccess_gauge = Gauge('purpleair_httpsuccess', 'PurpleAir air quality sesnor HTTP successful requests', ["sensor_host", "sensor_id"])  # httpsuccess
purpleair_httpsends_gauge = Gauge('purpleair_httpsends', 'PurpleAir air quality sesnor HTTP sends', ["sensor_host", "sensor_id"])  # httpsends

gauges = {
    'purpleair_temp_gauge': purpleair_temp_gauge,
    'purpleair_humidity_gauge': purpleair_humidity_gauge,
    'purpleair_dewpoint_gauge': purpleair_dewpoint_gauge,
    'purpleair_pressure_gauge': purpleair_pressure_gauge,
    'purpleair_pm25aqi_gauge': purpleair_pm25aqi_gauge,
    'purpleair_httpsuccess_gauge': purpleair_httpsuccess_gauge,
    'purpleair_httpsends_gauge': purpleair_httpsends_gauge,
}
