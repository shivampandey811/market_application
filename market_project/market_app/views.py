from django.shortcuts import redirect, render
from .models import Order
from dotenv import load_dotenv
import os
import pyotp
from helper_files.api_helper import ShoonyaApiPy
from django.http import JsonResponse
from django.core.paginator import Paginator
# Load environment variables from .env
load_dotenv()

def login_to_api():
    api = ShoonyaApiPy()    
    # Fetch credentials from environment variables
    uid = os.getenv('SHOONYA_UID')
    pwd = os.getenv('SHOONYA_PWD')
    vc = os.getenv('SHOONYA_VC')
    app_key = os.getenv('SHOONYA_APP_KEY')
    imei = os.getenv('SHOONYA_IMEI')
    token = os.getenv('SHOONYA_TOKEN')

    # Generate OTP for 2FA
    otp = pyotp.TOTP(token).now()
    factor2 = otp

    # Make the API login call
    ret = api.login(userid=uid, password=pwd, vendor_code=vc, twoFA=factor2, api_secret=app_key, imei=imei)
    
    return api

def home(request):    
    api = login_to_api()
    
    if request.method == 'POST':
        symbol = request.POST['symbol']
        exchange = request.POST['exchange']
        buy_or_sell = request.POST['buy_or_sell']
        product_type = request.POST['product_type']
        quantity = int(request.POST['quantity'])
        order_type = request.POST['order_type']
        price = float(request.POST['price']) if order_type == 'LMT' else 0

        # Place order via API
        order_response = api.place_order(
            buy_or_sell=buy_or_sell,
            product_type=product_type,
            exchange=exchange,
            tradingsymbol=symbol,
            quantity=quantity,
            discloseqty=0,
            price_type=order_type,
            price=price,
            trigger_price=None,
            retention='DAY',
            remarks=f'{buy_or_sell} {symbol} via Web Interface'
        )

        # Save order to DB
        Order.objects.create(
            symbol=symbol,
            quantity=quantity,
            order_type=order_type,
            price=price,
            buy_or_sell=buy_or_sell,
            exchange=exchange,
            product_type=product_type
        )

        return redirect('home')

    indices = {
        'Nifty 50': api.get_quotes(exchange='NSE', token='26000'),
        'Nifty Bank': api.get_quotes(exchange='NSE', token='26009'),
        'Sensex': api.get_quotes(exchange='BSE', token='BSE30')
    }
    orders = Order.objects.all().order_by('-created_at')
    print(orders)
    paginator = Paginator(orders, 10)  # Show 10 orders per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'indices': indices, 'page_obj': page_obj})

def get_indices_prices(request):
    api = login_to_api()
    
    indices = {
        'Nifty 50': api.get_quotes(exchange='NSE', token='26000'),
        'Nifty Bank': api.get_quotes(exchange='NSE', token='26009'),
        'Sensex': api.get_quotes(exchange='BSE', token='BSE30')
    }
    
    prices = {
        'Nifty 50': indices['Nifty 50']['lp'] if indices['Nifty 50'] else None,
        'Nifty Bank': indices['Nifty Bank']['lp'] if indices['Nifty Bank'] else None,
        'Sensex': indices['Sensex']['lp'] if indices['Sensex'] else None
    }
    
    return JsonResponse(prices)
