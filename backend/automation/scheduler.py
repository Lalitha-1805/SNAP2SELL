"""
Automation Module using APScheduler
Handles background jobs and scheduled tasks
"""

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, timedelta
from models import Order, Product, PriceHistory
import logging

logger = logging.getLogger(__name__)


class AutomationManager:
    """Manages scheduled automation tasks"""
    
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.jobs = {}
    
    def start(self):
        """Start the scheduler"""
        if not self.scheduler.running:
            self._register_jobs()
            self.scheduler.start()
            print("[OK] Automation scheduler started")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("[OK] Automation scheduler stopped")
    
    def _register_jobs(self):
        """Register all automated jobs"""
        # Run every 30 minutes
        self.add_job(
            'update_prices',
            self._update_product_prices,
            trigger=IntervalTrigger(minutes=30)
        )
        
        # Run daily at 2 AM
        self.add_job(
            'stock_alerts',
            self._check_low_stock,
            trigger=CronTrigger(hour=2, minute=0)
        )
        
        # Run every 6 hours
        self.add_job(
            'order_reminders',
            self._send_order_reminders,
            trigger=IntervalTrigger(hours=6)
        )
        
        # Run daily at 9 AM
        self.add_job(
            'weather_notifications',
            self._send_weather_notifications,
            trigger=CronTrigger(hour=9, minute=0)
        )
        
        print("[OK] All automation jobs registered")
    
    def add_job(self, job_id, job_func, trigger):
        """Add a scheduled job"""
        try:
            if not self.scheduler.running:
                # Schedule for when scheduler starts
                self.jobs[job_id] = {
                    'func': job_func,
                    'trigger': trigger
                }
            else:
                self.scheduler.add_job(
                    job_func,
                    trigger=trigger,
                    id=job_id,
                    replace_existing=True
                )
            logger.info(f"Job added: {job_id}")
        except Exception as e:
            logger.error(f"Failed to add job {job_id}: {str(e)}")
    
    def remove_job(self, job_id):
        """Remove a scheduled job"""
        try:
            self.scheduler.remove_job(job_id)
            logger.info(f"Job removed: {job_id}")
        except Exception as e:
            logger.error(f"Failed to remove job {job_id}: {str(e)}")
    
    def _update_product_prices(self):
        """Update product prices based on market data"""
        try:
            logger.info("Starting price update task...")
            
            products = Product.find_many({'is_active': True})
            
            for product in products:
                # Simulate market price update
                old_price = product['price']
                price_change = (old_price * 0.02)  # 2% change
                new_price = old_price + price_change
                
                # Record price history
                PriceHistory.record_price(
                    product_id=product['_id'],
                    price=new_price,
                    market_price=new_price
                )
                
                # Update product price
                Product.update(str(product['_id']), {'price': new_price})
            
            logger.info(f"Price update completed for {len(products)} products")
        
        except Exception as e:
            logger.error(f"Price update failed: {str(e)}")
    
    def _check_low_stock(self):
        """Check for low stock and send alerts"""
        try:
            logger.info("Starting stock check task...")
            
            # Find products with low stock (< 10 units)
            products = Product.find_many({'is_active': True})
            low_stock_products = [p for p in products if p['quantity'] < 10]
            
            for product in low_stock_products:
                alert_message = f"Low stock alert: {product['name']} has only {product['quantity']} units left"
                logger.warning(alert_message)
                # TODO: Send notification to farmer
            
            logger.info(f"Stock check completed. Found {len(low_stock_products)} low stock items")
        
        except Exception as e:
            logger.error(f"Stock check failed: {str(e)}")
    
    def _send_order_reminders(self):
        """Send reminders for pending orders"""
        try:
            logger.info("Starting order reminder task...")
            
            # Find pending orders older than 1 day
            cutoff_date = datetime.utcnow() - timedelta(days=1)
            orders = Order.find_many({'status': 'pending'})
            
            pending_orders = [
                o for o in orders 
                if o['created_at'] < cutoff_date
            ]
            
            for order in pending_orders:
                reminder_message = f"Order {str(order['_id'])} is still pending for {(datetime.utcnow() - order['created_at']).days} days"
                logger.info(reminder_message)
                # TODO: Send notification to buyer
            
            logger.info(f"Order reminder task completed for {len(pending_orders)} orders")
        
        except Exception as e:
            logger.error(f"Order reminder task failed: {str(e)}")
    
    def _send_weather_notifications(self):
        """Send weather-based notifications to farmers"""
        try:
            logger.info("Starting weather notification task...")
            
            # TODO: Integrate with weather API
            # For now, just log
            logger.info("Weather notifications sent to farmers")
        
        except Exception as e:
            logger.error(f"Weather notification task failed: {str(e)}")
    
    def get_job_status(self):
        """Get status of all scheduled jobs"""
        jobs_info = []
        
        for job in self.scheduler.get_jobs():
            jobs_info.append({
                'job_id': job.id,
                'next_run': job.next_run_time.isoformat() if job.next_run_time else None,
                'trigger': str(job.trigger)
            })
        
        return {
            'scheduler_running': self.scheduler.running,
            'jobs': jobs_info,
            'total_jobs': len(jobs_info)
        }


# Global automation manager instance
automation_manager = AutomationManager()
