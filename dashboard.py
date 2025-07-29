"""
Monitoring dashboard template for Test-monitoring_setup
"""

def render_monitoring_dashboard():
    """Render monitoring dashboard HTML"""
    return """
    <div class="bg-white shadow rounded-lg p-6">
        <h3 class="text-lg font-medium text-gray-900 mb-4">Performance Metrics</h3>
        <div id="performance-stats" hx-get="/api/monitoring/stats" hx-trigger="load, every 30s">
            <div class="animate-pulse">
                <div class="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                <div class="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                <div class="h-4 bg-gray-200 rounded w-5/6"></div>
            </div>
        </div>
    </div>
    """
