"""
TUI界面屏幕
"""
from .dashboard import DashboardScreen
from .daily import DailyScreen
from .diagnose import DiagnoseScreen
from .report import ReportScreen
from .scan import ScanScreen

__all__ = [
    "DashboardScreen",
    "DailyScreen",
    "DiagnoseScreen",
    "ReportScreen",
    "ScanScreen",
]
