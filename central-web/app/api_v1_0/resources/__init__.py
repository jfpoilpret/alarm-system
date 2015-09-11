# encoding: utf-8

# import all resources
from .users import UsersResource, UserResource
from .configurations import ConfigurationsResource, ConfigurationResource
from .configurations import CurrentConfigurationResource, ConfigurationMapResource
from .devices import DevicesResource, DeviceResource
from .thresholds import NoPingAlertThresholdsResource, VoltageAlertThresholdsResource
from .monitor import MonitorAlertsResource, MonitorDevicesResource, MonitorMapResource, MonitorStatusResource
from .alerts_history import AlertsHistoryResource
from .token import TokenResource
