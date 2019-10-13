from prometheus_client.metrics_core import GaugeMetricFamily

from app.repository.base import Repository


class TodosCollector:
    """
    Custom Prometheus collector to export custom metrics.
    The metrics are collected whenever the /metrics endpoint is called.
    """

    def __init__(self, repository: Repository):
        self._repository = repository

    def collect(self):
        stats = self._repository.stats()

        gauge = GaugeMetricFamily(
            name="app_current_todos",
            documentation="Number of Todos currently in the system, grouped by status.",
            labels=("status",),
        )
        gauge.add_metric(labels=("active",), value=stats.active)
        gauge.add_metric(labels=("inactive",), value=stats.inactive)

        yield gauge
