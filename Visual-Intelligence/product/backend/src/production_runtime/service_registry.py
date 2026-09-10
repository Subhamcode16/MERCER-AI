"""
Phase 23 Service Registry for Runtime Components.
"""
from typing import Dict, Any, Optional, Callable
import logging

logger = logging.getLogger(__name__)

class ServiceRegistry:
    """Central registry for managing initialized runtime services and singletons."""
    _instance: Optional["ServiceRegistry"] = None

    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}

    @classmethod
    def get_instance(cls) -> "ServiceRegistry":
        if cls._instance is None:
            cls._instance = ServiceRegistry()
        return cls._instance

    @classmethod
    def reset(cls) -> None:
        cls._instance = None

    def register(self, service_name: str, instance: Any) -> None:
        self._services[service_name] = instance
        logger.info(f"Registered service: {service_name}")

    def register_factory(self, service_name: str, factory: Callable[[], Any]) -> None:
        self._factories[service_name] = factory

    def get(self, service_name: str) -> Optional[Any]:
        if service_name in self._services:
            return self._services[service_name]
        if service_name in self._factories:
            instance = self._factories[service_name]()
            self._services[service_name] = instance
            return instance
        return None

    def list_services(self) -> Dict[str, str]:
        return {k: type(v).__name__ for k, v in self._services.items()}
