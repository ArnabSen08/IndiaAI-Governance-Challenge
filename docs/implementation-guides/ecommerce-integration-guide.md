# E-Commerce Platform Integration Guide

## 1. Integration Architecture Overview

### 1.1 Multi-Platform Integration Strategy

```
┌─────────────────────────────────────────────────────┐
│         SML Platform Core                           │
│  (Product Management, Pricing, Inventory)           │
└──────────┬──────────────────────────────────────────┘
           │
           │ Unified API Layer
           │
    ┌──────┴────────────────────────────────────┐
    │                                            │
    ▼                                            ▼
API Adapter Layer         Event Bus / Message Queue
    │                           │
    ├─ Amazon Adapter          Kafka/RabbitMQ
    ├─ Flipkart Adapter        │
    ├─ IndiaMART Adapter       ├─ Price Change Events
    ├─ GeM Adapter             ├─ Order Events
    └─ Website Adapter         ├─ Inventory Events
                                └─ Rating Events
                                     │
                                     ▼
                            Downstream Services
                            (Analytics, Notifications)
```

---

## 2. Platform-Specific Integration Details

### 2.1 Amazon Seller Central

#### 2.1.1 Authentication
```python
import requests
from requests_auth import HTTPSignatureAuth
import hashlib
import hmac
from datetime import datetime

class AmazonSellerAPI:
    """Amazon SP-API (Selling Partner API) Integration"""
    
    def __init__(self, client_id, client_secret, region='INDIA'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.region = region
        self.access_token = None
        self.token_expiry = None
        self.base_url = "https://sellingpartnerapi-in.amazon.com"
        
        # Refresh token from secure storage
        self.refresh_token = self.get_refresh_token_from_vault()
    
    def get_access_token(self):
        """Get OAuth 2.0 access token"""
        if self.access_token and datetime.now() < self.token_expiry:
            return self.access_token
        
        auth_url = "https://api.amazon.com/auth/o2/token"
        
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        
        data = response.json()
        self.access_token = data['access_token']
        self.token_expiry = datetime.now() + timedelta(hours=1)
        
        return self.access_token
    
    def create_product_listing(self, product_data):
        """Create new product listing on Amazon"""
        
        endpoint = f"{self.base_url}/catalog/2022-04-01/items"
        
        payload = {
            "productType": "BOOK",  # Can be customized
            "attributes": {
                "title": [{"value": product_data['name']}],
                "brand": [{"value": product_data.get('brand', 'Self-Help Group')}],
                "description": [{"value": product_data['description'][:2000]}],
                "condition_type": [{"value": "New"}],
                "item_type": [{"value": "BOOK"}],
                "bullet_point": [
                    {"value": bp} for bp in product_data.get('bullet_points', [])
                ],
                "images": [
                    {"value": img_url} for img_url in product_data['image_urls']
                ],
                "base_price": [{"currency": "INR", "value": product_data['price']}]
            }
        }
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    
    def update_product_pricing(self, asin, new_price):
        """Update product price on Amazon"""
        
        endpoint = f"{self.base_url}/pricing/2022-05-01/pricing/items/{asin}"
        
        payload = {
            "selectedSku": asin,
            "pricing": [
                {
                    "status": "Active",
                    "fulfillmentChannel": "DEFAULT",
                    "offerType": "B2C",
                    "currency": "INR",
                    "listingPrice": {
                        "amount": new_price
                    },
                    "strikethrough": {
                        "amount": new_price * 1.2  # 20% higher as MRP
                    }
                }
            ]
        }
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        response = requests.patch(endpoint, json=payload, headers=headers)
        return response.json()
    
    def get_orders(self, days_back=7):
        """Fetch recent orders from Amazon"""
        
        endpoint = f"{self.base_url}/orders/v0/orders"
        
        params = {
            'CreatedAfter': (datetime.now() - timedelta(days=days_back)).isoformat(),
            'OrderStatuses': 'Pending,Unshipped,PartiallyShipped'
        }
        
        headers = {
            'Authorization': f'Bearer {self.get_access_token()}',
            'x-amz-date': datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        }
        
        response = requests.get(endpoint, params=params, headers=headers)
        return response.json()['payload']['Orders']
```

#### 2.1.2 Inventory Synchronization
```python
def sync_inventory_to_amazon(product_id, available_quantity):
    """Sync inventory levels to Amazon"""
    
    amazon_api = AmazonSellerAPI(client_id, client_secret)
    
    # Get ASIN mapping
    asin = get_asin_for_product(product_id)
    
    # Update inventory
    endpoint = f"{amazon_api.base_url}/fulfillment-inbound-v0/inboundShipments"
    
    inventory_payload = {
        "MarketplaceId": "A21TJRUUN4KGV",  # India
        "SellerSKU": product_id,
        "QuantityAvailable": available_quantity,
        "FulfillmentNetworkSKU": asin
    }
    
    response = requests.put(
        endpoint,
        json=inventory_payload,
        headers={'Authorization': f'Bearer {amazon_api.get_access_token()}'}
    )
    
    return response.status_code == 200
```

### 2.2 Flipkart Seller Integration

#### 2.2.1 Authentication & API Setup
```python
import requests
from datetime import datetime, timedelta

class FlipkartSellerAPI:
    """Flipkart Seller Hub API Integration"""
    
    def __init__(self, seller_id, auth_token):
        self.seller_id = seller_id
        self.auth_token = auth_token
        self.base_url = "https://api.flipkart.com/sellers"
        self.headers = {
            'Authorization': f'Bearer {auth_token}',
            'Content-Type': 'application/json'
        }
    
    def list_product(self, product_data):
        """List product on Flipkart"""
        
        endpoint = f"{self.base_url}/{self.seller_id}/products"
        
        payload = {
            "fsn": product_data.get('fsn', generate_fsn()),
            "productTitle": product_data['name'],
            "description": product_data['description'],
            "category": product_data['category'],
            "hsn": product_data.get('hsn_code', ''),
            "productBrand": product_data.get('brand', ''),
            "specifications": {
                "brand": product_data.get('brand', ''),
                "model": product_data.get('model', ''),
                "color": product_data.get('color', 'N/A'),
                "material": product_data.get('material', 'N/A')
            },
            "images": product_data['image_urls'],
            "price": {
                "mrp": product_data.get('mrp', product_data['price'] * 1.2),
                "selling": product_data['price']
            },
            "weight": product_data.get('weight_grams', 0),
            "dimensions": {
                "length": product_data.get('length_cm', 0),
                "breadth": product_data.get('breadth_cm', 0),
                "height": product_data.get('height_cm', 0)
            },
            "packaging": {
                "quantity": product_data.get('units_per_box', 1),
                "weight": product_data.get('package_weight_grams', product_data.get('weight_grams', 0))
            },
            "sku": [{
                "skuId": product_data['sku'],
                "price": product_data['price'],
                "quantity": product_data['available_quantity'],
                "attributes": {
                    "size": product_data.get('size', 'Standard'),
                    "color": product_data.get('color', 'N/A')
                }
            }]
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        return response.json()
    
    def update_inventory(self, sku_id, quantity):
        """Update product inventory"""
        
        endpoint = f"{self.base_url}/{self.seller_id}/inventory"
        
        payload = {
            "inventory": [{
                "skuId": sku_id,
                "quantity": quantity
            }]
        }
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        return response.json()
    
    def fetch_orders(self, order_status='UNSHIPPED'):
        """Fetch orders from Flipkart"""
        
        endpoint = f"{self.base_url}/{self.seller_id}/orders"
        
        params = {
            'status': order_status,
            'limit': 100
        }
        
        response = requests.get(endpoint, params=params, headers=self.headers)
        return response.json()['orders']
```

### 2.3 IndiaMART Integration

#### 2.3.1 IndiaMART B2B API
```python
class IndiarMartAPI:
    """IndiaMART B2B Platform Integration"""
    
    def __init__(self, merchant_id, api_key):
        self.merchant_id = merchant_id
        self.api_key = api_key
        self.base_url = "https://api.indiamart.com/v2"
    
    def create_product_listing(self, product_data):
        """Create product listing on IndiaMART"""
        
        endpoint = f"{self.base_url}/products"
        
        payload = {
            "merchant_id": self.merchant_id,
            "product_name": product_data['name'],
            "product_description": product_data['description'],
            "hs_code": product_data.get('hs_code', ''),
            "categories": product_data['categories'],
            "product_images": product_data['image_urls'],
            "moq": product_data.get('minimum_order_quantity', 1),
            "price_range": {
                "minimum": product_data['price'],
                "maximum": product_data['price'] * 1.5
            },
            "certifications": product_data.get('certifications', []),
            "sustainability_score": product_data.get('sustainability_score', 0),
            "geo_locations": [product_data['location']],
            "delivery_time_days": product_data.get('delivery_days', 5)
        }
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    
    def get_buyer_inquiries(self):
        """Fetch buyer inquiries/RFQs"""
        
        endpoint = f"{self.base_url}/inquiries"
        
        params = {
            'merchant_id': self.merchant_id,
            'status': 'open'
        }
        
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        response = requests.get(endpoint, params=params, headers=headers)
        return response.json()['inquiries']
    
    def send_quote_response(self, inquiry_id, quotation_data):
        """Send quotation response to buyer inquiry"""
        
        endpoint = f"{self.base_url}/inquiries/{inquiry_id}/quote"
        
        payload = {
            "merchant_id": self.merchant_id,
            "quantity": quotation_data['quantity'],
            "unit_price": quotation_data['unit_price'],
            "total_price": quotation_data['total_price'],
            "delivery_days": quotation_data.get('delivery_days', 5),
            "payment_terms": quotation_data.get('payment_terms', 'NET30'),
            "validity_days": quotation_data.get('validity_days', 7),
            "message": quotation_data.get('message', '')
        }
        
        headers = {'Authorization': f'Bearer {self.api_key}'}
        
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
```

### 2.4 Government e-Marketplace (GeM) Integration

#### 2.4.1 GeM API Integration
```python
class GeMarketplaceAPI:
    """Government e-Marketplace (GeM) Integration"""
    
    def __init__(self, organization_id, api_key, sandbox=False):
        self.organization_id = organization_id
        self.api_key = api_key
        self.base_url = "https://api.sandbox.gem.gov.in" if sandbox \
                       else "https://api.gem.gov.in"
    
    def register_seller(self, organization_details):
        """Register SHG as seller on GeM"""
        
        endpoint = f"{self.base_url}/v2/sellers/registration"
        
        payload = {
            "organization_name": organization_details['name'],
            "organization_type": "MSME",  # Micro and Small Enterprises
            "address": organization_details['address'],
            "contact_person": organization_details['contact'],
            "email": organization_details['email'],
            "phone": organization_details['phone'],
            "pan": organization_details.get('pan', ''),
            "gst": organization_details.get('gst', ''),
            "banking_details": organization_details['bank_details'],
            "documents": {
                "registration_certificate": organization_details['cert_url'],
                "bank_document": organization_details['bank_doc_url']
            }
        }
        
        headers = {'api_key': self.api_key}
        
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    
    def search_tenders(self, category=None, state=None):
        """Search for government tenders matching SHG products"""
        
        endpoint = f"{self.base_url}/v2/tenders/search"
        
        params = {
            'category': category,
            'state': state,
            'status': 'ACTIVE',
            'limit': 100
        }
        
        headers = {'api_key': self.api_key}
        
        response = requests.get(endpoint, params=params, headers=headers)
        return response.json()['tenders']
    
    def submit_tender_bid(self, tender_id, bid_data):
        """Submit bid for government tender"""
        
        endpoint = f"{self.base_url}/v2/tenders/{tender_id}/bid"
        
        payload = {
            "seller_id": self.organization_id,
            "unit_price": bid_data['unit_price'],
            "total_price": bid_data['total_price'],
            "quantity": bid_data['quantity'],
            "delivery_location": bid_data['delivery_location'],
            "delivery_days": bid_data.get('delivery_days', 15),
            "warranty": bid_data.get('warranty', ''),
            "terms_conditions": bid_data.get('terms', '')
        }
        
        headers = {'api_key': self.api_key}
        
        response = requests.post(endpoint, json=payload, headers=headers)
        return response.json()
    
    def track_tender_status(self, tender_id):
        """Track tender bidding status"""
        
        endpoint = f"{self.base_url}/v2/tenders/{tender_id}/status"
        
        headers = {'api_key': self.api_key}
        
        response = requests.get(endpoint, headers=headers)
        return response.json()
```

---

## 3. Order Management & Fulfillment

### 3.1 Unified Order Processing

```python
class UnifiedOrderManager:
    """Manage orders across multiple platforms"""
    
    def __init__(self):
        self.amazon_api = AmazonSellerAPI(...)
        self.flipkart_api = FlipkartSellerAPI(...)
        self.indiamart_api = IndiarMartAPI(...)
        self.gem_api = GeMarketplaceAPI(...)
    
    def fetch_all_orders(self):
        """Fetch orders from all active platforms"""
        
        all_orders = []
        
        # Fetch from each platform
        try:
            amazon_orders = self.amazon_api.get_orders()
            all_orders.extend(self.normalize_amazon_orders(amazon_orders))
        except Exception as e:
            logger.error(f"Failed to fetch Amazon orders: {e}")
        
        try:
            flipkart_orders = self.flipkart_api.fetch_orders()
            all_orders.extend(self.normalize_flipkart_orders(flipkart_orders))
        except Exception as e:
            logger.error(f"Failed to fetch Flipkart orders: {e}")
        
        try:
            indiamart_inquiries = self.indiamart_api.get_buyer_inquiries()
            all_orders.extend(self.normalize_indiamart_inquiries(indiamart_inquiries))
        except Exception as e:
            logger.error(f"Failed to fetch IndiaMART inquiries: {e}")
        
        return all_orders
    
    def normalize_amazon_orders(self, orders):
        """Normalize Amazon orders to common format"""
        
        normalized = []
        for order in orders:
            normalized.append({
                'platform': 'amazon',
                'order_id': order['AmazonOrderId'],
                'buyer_name': order['BuyerName'],
                'order_date': order['PurchaseDate'],
                'items': [
                    {
                        'product_id': item['SellerSKU'],
                        'quantity': item['QuantityOrdered'],
                        'price': item['ItemPrice']['Amount']
                    }
                    for item in order['OrderItems']
                ],
                'total_value': order['OrderTotal']['Amount'],
                'status': order['OrderStatus'],
                'shipping_address': order['ShippingAddress'],
                'payment_method': 'Online'
            })
        return normalized
    
    def create_order_in_database(self, order):
        """Store normalized order in database"""
        
        db_order = Order(
            platform_order_id=order['order_id'],
            platform=order['platform'],
            buyer_id=self.get_or_create_buyer(order['buyer_name']),
            shg_id=self.get_shg_from_products(order['items']),
            total_value=order['total_value'],
            order_date=order['order_date'],
            status=order['status'],
            shipping_address=order['shipping_address'],
            payment_method=order['payment_method']
        )
        
        db.session.add(db_order)
        db.session.commit()
        
        # Create order items
        for item in order['items']:
            order_item = OrderItem(
                order_id=db_order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                unit_price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        return db_order.id
    
    def update_order_status(self, order_id, new_status):
        """Update order status across platform and database"""
        
        order = db.session.query(Order).filter_by(id=order_id).first()
        
        if order.platform == 'amazon':
            # Amazon status updates might require specific handling
            pass
        elif order.platform == 'flipkart':
            self.flipkart_api.update_order_status(order.platform_order_id, new_status)
        elif order.platform == 'indiamart':
            # IndiaMART order management
            pass
        
        order.status = new_status
        order.updated_at = datetime.now()
        db.session.commit()
```

---

## 4. Real-time Sync with Message Queues

### 4.1 Event-Driven Architecture

```python
from kafka import KafkaProducer, KafkaConsumer
import json

class EcommerceEventHandler:
    """Handle real-time events from e-commerce platforms"""
    
    def __init__(self, kafka_brokers):
        self.producer = KafkaProducer(
            bootstrap_servers=kafka_brokers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.consumer = KafkaConsumer(
            'ecommerce-events',
            bootstrap_servers=kafka_brokers,
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )
    
    def publish_order_event(self, order):
        """Publish order event"""
        self.producer.send('ecommerce-events', {
            'event_type': 'ORDER_CREATED',
            'timestamp': datetime.now().isoformat(),
            'order': order
        })
    
    def publish_inventory_sync_event(self, product_id, quantity):
        """Publish inventory sync event"""
        self.producer.send('ecommerce-events', {
            'event_type': 'INVENTORY_UPDATED',
            'timestamp': datetime.now().isoformat(),
            'product_id': product_id,
            'quantity': quantity
        })
    
    def consume_events(self):
        """Consume events from Kafka"""
        for event in self.consumer:
            if event['event_type'] == 'ORDER_CREATED':
                self.handle_order_creation(event['order'])
            elif event['event_type'] == 'INVENTORY_UPDATED':
                self.handle_inventory_update(event['product_id'], event['quantity'])
```

---

## 5. Monitoring & Health Checks

### 5.1 Integration Health Monitoring

```python
class IntegrationHealthMonitor:
    """Monitor health of e-commerce integrations"""
    
    def __init__(self):
        self.amazon_api = AmazonSellerAPI(...)
        self.flipkart_api = FlipkartSellerAPI(...)
        self.indiamart_api = IndiarMartAPI(...)
        self.gem_api = GeMarketplaceAPI(...)
    
    def check_api_health(self):
        """Check health of all API connections"""
        
        health_status = {}
        
        # Check Amazon
        try:
            self.amazon_api.get_access_token()
            health_status['amazon'] = 'HEALTHY'
        except Exception as e:
            health_status['amazon'] = f'ERROR: {str(e)}'
        
        # Check Flipkart
        try:
            response = requests.get(
                f"{self.flipkart_api.base_url}/health",
                headers=self.flipkart_api.headers
            )
            health_status['flipkart'] = 'HEALTHY' if response.status_code == 200 else 'ERROR'
        except Exception as e:
            health_status['flipkart'] = f'ERROR: {str(e)}'
        
        # Check IndiaMART
        try:
            response = requests.get(
                f"{self.indiamart_api.base_url}/health",
                headers={'Authorization': f'Bearer {self.indiamart_api.api_key}'}
            )
            health_status['indiamart'] = 'HEALTHY' if response.status_code == 200 else 'ERROR'
        except Exception as e:
            health_status['indiamart'] = f'ERROR: {str(e)}'
        
        # Check GeM
        try:
            response = requests.get(
                f"{self.gem_api.base_url}/health",
                headers={'api_key': self.gem_api.api_key}
            )
            health_status['gem'] = 'HEALTHY' if response.status_code == 200 else 'ERROR'
        except Exception as e:
            health_status['gem'] = f'ERROR: {str(e)}'
        
        return health_status
    
    def monitor_sync_latency(self):
        """Monitor data sync latency between platforms"""
        
        # Test order fetch latency
        start_time = time.time()
        orders = self.fetch_all_orders()
        latency = time.time() - start_time
        
        metrics = {
            'total_orders': len(orders),
            'sync_latency_seconds': latency,
            'orders_per_second': len(orders) / latency if latency > 0 else 0
        }
        
        # Alert if latency exceeds threshold
        if latency > 300:  # 5 minutes
            send_alert(f"Order sync latency exceeded threshold: {latency}s")
        
        return metrics
```

