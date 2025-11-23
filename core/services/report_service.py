from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, List, Optional
from datetime import date, datetime, timedelta

from core.repositories.invoice_repository import InvoiceRepository
from core.repositories.invoice_item_repository import InvoiceItemRepository
from core.repositories.product_repository import ProductRepository

class ReportService:
    def __init__(self, db: Session):
        self.db= db
        self.invoice_repo= InvoiceRepository(db)
        self.invoice_item_repo= InvoiceItemRepository(db)
        self.product_repo= ProductRepository(db)

    def get_daily_sales_report(self, target_date: Optional[date]= None)->Dict:
        if target_date is None:
            target_date= date.today()
        
        try:
            invoices= self.invoice_repo.list_by_date_range(target_date, target_date)

            total_sales= sum(getattr(inv, "total", 0) for inv in invoices)
            total_invoices= len(invoices)
            average_invoice= total_sales/ total_invoices if total_invoices > 0 else 0

            return {
                "date": target_date,
                "total_sales": total_sales,
                "total_invoices": total_invoices,
                "average_invoice": average_invoice,
                "invoices": invoices,
            }
        
        except SQLAlchemyError as e:
            return {
                "date": target_date,
                "total_sales": 0,
                "total_invoices": 0,
                "average_invoice": 0,
                "invoices": []
            }
        
    def get_monthly_sales_report(self, year:int, month:int)->Dict:
        try:
            start_date= date(year, month, 1)
            end_date = (
                date(year + 1, 1, 1) - timedelta(days=1)
                if month == 12
                else date(year, month + 1, 1) - timedelta(days=1)
            )

            invoices= self.invoice_repo.list_by_date_range(start_date, end_date)

            total_sales= sum(getattr(inv, "total", 0) for inv in invoices)
            total_invoices= len(invoices)
            average_invoices= total_sales / total_invoices if total_invoices > 0 else 0

            daily_sales: Dict[date, float]= {}
            for inv in invoices:
                inv_date= inv.date.date() if isinstance(inv.date, datetime) else inv.date
                daily_sales.setdefault(inv_date, 0)
                daily_sales[inv_date]+= getattr(inv, "total", 0)

            return {
                "year": year,
                "month": month,
                "start_date": start_date,
                "end_date": end_date,
                "total_sales": total_sales,
                "total_invoices": total_invoices,
                "average_invoices": average_invoices,
                "daily_sales": daily_sales
            }
        
        except SQLAlchemyError as e:
            return {}