"""
Currency Conversion Service for Drink-X Cellar Management

This module provides currency conversion functionality using the forex-python package.
It handles conversion of purchase prices and current market values to USD for 
consistent dashboard calculations and analytics.

Dependencies:
    - forex-python==1.8

Usage:
    from currencyService import currency_converter
    
    usd_amount = currency_converter.convert_to_usd(100, 'EUR')
    rate = currency_converter.get_exchange_rate('GBP', 'USD')
"""

from forex_python.converter import CurrencyConverter, CurrencyRates
from forex_python.bitcoin import BtcConverter
from datetime import datetime, timedelta
import logging
import json
from decimal import Decimal, InvalidOperation

# Configure logging for currency service
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CellarCurrencyConverter:
    """
    Enhanced currency converter for cellar management system.
    Provides USD conversion with caching, error handling, and fallback mechanisms.
    """
    
    def __init__(self):
        """Initialize the currency converter with caching capabilities."""
        self.converter = CurrencyConverter()
        self.rates = CurrencyRates()
        self.btc_converter = BtcConverter()  # For cryptocurrency support if needed
        
        # Cache settings
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache rates for 1 hour
        self.last_cache_cleanup = datetime.now()
        self.cache_cleanup_interval = timedelta(hours=6)  # Cleanup old cache every 6 hours
        
        # Fallback exchange rates (approximate rates as of 2024)
        # These are used when API calls fail
        self.fallback_rates = {
            'USD': 1.0,
            'EUR': 1.10,
            'GBP': 1.25,
            'SGD': 0.74,
            'JPY': 0.0067,
            'AUD': 0.66,
            'CAD': 0.74,
            'CHF': 1.12,
            'CNY': 0.14,
            'HKD': 0.13,
            'KRW': 0.00075,
            'MYR': 0.22,
            'THB': 0.028,
            'VND': 0.000041,
            'INR': 0.012,
            'TWD': 0.031,
            'NZD': 0.61,
            'SEK': 0.096,
            'NOK': 0.092,
            'DKK': 0.15,
            'PLN': 0.25,
            'CZK': 0.044,
            'HUF': 0.0027,
            'RUB': 0.011,
            'BRL': 0.18,
            'MXN': 0.058,
            'ZAR': 0.053,
            'TRY': 0.030,
        }
        
        # Supported currencies (ISO 4217 codes)
        self.supported_currencies = set(self.fallback_rates.keys())
        
        logger.info("CellarCurrencyConverter initialized successfully")
    
    def _cleanup_cache(self):
        """Remove expired entries from cache."""
        now = datetime.now()
        if now - self.last_cache_cleanup > self.cache_cleanup_interval:
            expired_keys = []
            for key, data in self.cache.items():
                if now - data['timestamp'] > self.cache_duration:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.cache[key]
            
            self.last_cache_cleanup = now
            if expired_keys:
                logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")
    
    def _get_cached_rate(self, from_currency, to_currency='USD'):
        """Get exchange rate from cache if available and fresh."""
        self._cleanup_cache()
        
        cache_key = f"{from_currency}_{to_currency}"
        now = datetime.now()
        
        if (cache_key in self.cache and 
            now - self.cache[cache_key]['timestamp'] < self.cache_duration):
            logger.debug(f"Using cached rate for {cache_key}")
            return self.cache[cache_key]['rate']
        
        return None
    
    def _cache_rate(self, from_currency, to_currency, rate):
        """Store exchange rate in cache."""
        cache_key = f"{from_currency}_{to_currency}"
        self.cache[cache_key] = {
            'rate': rate,
            'timestamp': datetime.now()
        }
        logger.debug(f"Cached rate for {cache_key}: {rate}")
    
    def _validate_currency_code(self, currency_code):
        """Validate currency code format and support."""
        if not currency_code or not isinstance(currency_code, str):
            return False
        
        currency_code = currency_code.upper().strip()
        
        # Check if it's a 3-letter ISO code
        if len(currency_code) != 3:
            logger.warning(f"Invalid currency code format: {currency_code}")
            return False
        
        return True
    
    def get_exchange_rate(self, from_currency, to_currency='USD'):
        """
        Get exchange rate between two currencies.
        
        Args:
            from_currency (str): Source currency code (e.g., 'EUR')
            to_currency (str): Target currency code (e.g., 'USD')
        
        Returns:
            float: Exchange rate or None if conversion fails
        """
        if not self._validate_currency_code(from_currency) or not self._validate_currency_code(to_currency):
            return None
        
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        
        # Same currency
        if from_currency == to_currency:
            return 1.0
        
        # Check cache first
        cached_rate = self._get_cached_rate(from_currency, to_currency)
        if cached_rate is not None:
            return cached_rate
        
        try:
            # Try to get rate from forex-python
            rate = self.rates.get_rate(from_currency, to_currency)
            
            # Cache the successful rate
            self._cache_rate(from_currency, to_currency, rate)
            
            logger.info(f"Successfully retrieved rate {from_currency} to {to_currency}: {rate}")
            return rate
            
        except Exception as e:
            logger.warning(f"API rate retrieval failed for {from_currency} to {to_currency}: {e}")
            
            # Try fallback calculation
            if from_currency in self.fallback_rates and to_currency in self.fallback_rates:
                # Convert via USD: from_currency -> USD -> to_currency
                from_usd_rate = self.fallback_rates[from_currency]
                to_usd_rate = self.fallback_rates[to_currency]
                fallback_rate = from_usd_rate / to_usd_rate
                
                logger.info(f"Using fallback rate {from_currency} to {to_currency}: {fallback_rate}")
                return fallback_rate
            
            logger.error(f"No fallback rate available for {from_currency} to {to_currency}")
            return None
    
    def convert_to_usd(self, amount, from_currency):
        """
        Convert amount from any currency to USD.
        
        Args:
            amount (float, int, Decimal, str): Amount to convert
            from_currency (str): Source currency code
        
        Returns:
            float: Amount in USD or None if conversion fails
        """
        # Handle None or empty values
        if amount is None or from_currency is None:
            return None
        
        # Validate and normalize currency code
        if not self._validate_currency_code(from_currency):
            logger.warning(f"Invalid currency code: {from_currency}")
            return None
        
        from_currency = from_currency.upper().strip()
        
        # Convert amount to float
        try:
            if isinstance(amount, str):
                amount = float(amount)
            elif isinstance(amount, Decimal):
                amount = float(amount)
            elif not isinstance(amount, (int, float)):
                logger.warning(f"Invalid amount type: {type(amount)}")
                return None
            
            amount = float(amount)
            
            # Check for negative amounts
            if amount < 0:
                logger.warning(f"Negative amount provided: {amount}")
                return None
                
        except (ValueError, InvalidOperation) as e:
            logger.warning(f"Could not convert amount to float: {amount}, error: {e}")
            return None
        
        # Handle USD (no conversion needed)
        if from_currency == 'USD':
            return amount
        
        # Get exchange rate
        exchange_rate = self.get_exchange_rate(from_currency, 'USD')
        
        if exchange_rate is None:
            logger.error(f"Could not get exchange rate for {from_currency} to USD")
            return None
        
        # Perform conversion
        usd_amount = amount * exchange_rate
        
        logger.debug(f"Converted {amount} {from_currency} to {usd_amount} USD (rate: {exchange_rate})")
        return round(usd_amount, 2)  # Round to 2 decimal places for currency
    
    def convert_amount(self, amount, from_currency, to_currency):
        """
        Convert amount between any two currencies.
        
        Args:
            amount (float, int, Decimal, str): Amount to convert
            from_currency (str): Source currency code
            to_currency (str): Target currency code
        
        Returns:
            float: Converted amount or None if conversion fails
        """
        if amount is None or from_currency is None or to_currency is None:
            return None
        
        # Validate currency codes
        if not self._validate_currency_code(from_currency) or not self._validate_currency_code(to_currency):
            return None
        
        from_currency = from_currency.upper().strip()
        to_currency = to_currency.upper().strip()
        
        # Same currency
        if from_currency == to_currency:
            try:
                return float(amount)
            except (ValueError, TypeError):
                return None
        
        # Convert via get_exchange_rate
        exchange_rate = self.get_exchange_rate(from_currency, to_currency)
        
        if exchange_rate is None:
            return None
        
        try:
            converted_amount = float(amount) * exchange_rate
            return round(converted_amount, 2)
        except (ValueError, TypeError) as e:
            logger.warning(f"Amount conversion failed: {e}")
            return None
    
    def get_supported_currencies(self):
        """Get list of supported currency codes."""
        return sorted(list(self.supported_currencies))
    
    def is_currency_supported(self, currency_code):
        """Check if a currency code is supported."""
        if not self._validate_currency_code(currency_code):
            return False
        return currency_code.upper() in self.supported_currencies
    
    def get_cache_info(self):
        """Get information about the current cache state."""
        return {
            'cached_rates': len(self.cache),
            'cache_duration_hours': self.cache_duration.total_seconds() / 3600,
            'last_cleanup': self.last_cache_cleanup.isoformat(),
            'cache_keys': list(self.cache.keys())
        }
    
    def clear_cache(self):
        """Clear all cached exchange rates."""
        cache_size = len(self.cache)
        self.cache.clear()
        logger.info(f"Cleared {cache_size} cached exchange rates")
    
    def batch_convert_to_usd(self, amounts_with_currencies):
        """
        Convert multiple amounts to USD in a single call.
        
        Args:
            amounts_with_currencies (list): List of tuples (amount, currency)
        
        Returns:
            list: List of USD amounts (None for failed conversions)
        """
        results = []
        
        for amount, currency in amounts_with_currencies:
            usd_amount = self.convert_to_usd(amount, currency)
            results.append(usd_amount)
        
        return results

# Global instance for use throughout the application
currency_converter = CellarCurrencyConverter()

# Example usage and testing
if __name__ == "__main__":
    # Test the currency converter
    print("Testing CellarCurrencyConverter...")
    
    # Test basic conversion
    print(f"100 EUR to USD: {currency_converter.convert_to_usd(100, 'EUR')}")
    print(f"50 GBP to USD: {currency_converter.convert_to_usd(50, 'GBP')}")
    print(f"1000 JPY to USD: {currency_converter.convert_to_usd(1000, 'JPY')}")
    
    # Test same currency
    print(f"100 USD to USD: {currency_converter.convert_to_usd(100, 'USD')}")
    
    # Test error cases
    print(f"Invalid currency: {currency_converter.convert_to_usd(100, 'INVALID')}")
    print(f"None amount: {currency_converter.convert_to_usd(None, 'EUR')}")
    
    # Test batch conversion
    batch_data = [(100, 'EUR'), (50, 'GBP'), (1000, 'JPY'), (100, 'USD')]
    batch_results = currency_converter.batch_convert_to_usd(batch_data)
    print(f"Batch conversion results: {batch_results}")
    
    # Test cache info
    print(f"Cache info: {currency_converter.get_cache_info()}")
    
    # Test supported currencies
    print(f"Supported currencies: {currency_converter.get_supported_currencies()}")
