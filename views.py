import logging
import hashlib
import time
from datetime import datetime
from django.db.models import Count
from django.shortcuts import render, redirect
from admins.models import Sendquery
from cyber_alert.models import GiverTransaction, AdminRegister


# Set up basic logging
logger = logging.getLogger(__name__)

# Blockchain Simulation

class SmartContract:
    """Simulates a basic blockchain smart contract."""

    def __init__(self):
        self.blockchain = []  # List to store blocks
        self.block_number = 0  # Simulated block number
    
    def create_block(self, action, data):
        """Simulates creating a new block in the blockchain."""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        block_data = {
            'block_number': self.block_number,
            'timestamp': timestamp,
            'action': action,
            'data': data,
            'transaction_hash': self.generate_transaction_hash(action, data)
        }
        self.blockchain.append(block_data)
        self.block_number += 1

        # Print the block creation log in the terminal
        self.print_blockchain_log(block_data)

    def generate_transaction_hash(self, action, data):
        """Generates a fake transaction hash using SHA256."""
        return hashlib.sha256(f"{self.block_number}{data}{action}".encode()).hexdigest()

    def print_blockchain_log(self, block_data):
        """Print the simulated blockchain log to the terminal."""
        print("\n[SMART CONTRACT LOG] - Blockchain Transaction")
        print(f"Block #{block_data['block_number']} - {block_data['timestamp']}")
        print(f"Action: {block_data['action']}")
        print(f"Data: {block_data['data']}")
        print(f"Transaction Hash: {block_data['transaction_hash']}")
        print("=" * 50)  # Separator to mimic blockchain blocks

    def get_blockchain(self):
        """Returns the list of all blocks."""
        return self.blockchain


# Instantiate the smart contract (blockchain) class
smart_contract = SmartContract()


# Blockchain Simulation Functions (Interacting with Smart Contracts)

def log_blockchain_action(action, data):
    """Simulates logging a transaction on a blockchain with smart contract-like logs."""
    smart_contract.create_block(action, data)


# Views with Blockchain Simulation

def admin_page(request):
    if request.method == "POST":
        admin = request.POST.get('admin')
        password = request.POST.get('password')
        if admin == "admin" and password == "admin":
            log_blockchain_action("Admin Login", f"Admin {admin} logged in successfully.")
            return redirect('analyze')
    
    return render(request, 'admins/admin_page.html')


def analyze(request):
    topic = GiverTransaction.objects.values('date', 'name').annotate(dcount=Count('month')).order_by('-dcount')
    
    # Blockchain-like smart contract interaction
    log_blockchain_action("Analyze Data", f"Analyzed transaction data and grouped by date and name.")

    return render(request, "admins/analyze.html", {'form': topic})


def adlogout(request):
    log_blockchain_action("Admin Logout", f"Admin logged out.")
    return redirect('admin_page')


def charts(request, chart_type):
    chart = GiverTransaction.objects.values('month').annotate(dcount=Count('month'))
    
    # Blockchain-like smart contract interaction
    log_blockchain_action("Chart Generation", f"Generated chart of type {chart_type}.")

    return render(request, "admins/charts.html", {'form': chart, 'chart_type': chart_type})


def riskuser(request):
    obj = GiverTransaction.objects.filter(amount__range=(500000, 2500000))
    
    # Blockchain-like smart contract interaction
    log_blockchain_action("Risk User Analysis", f"Identified users with transaction amounts between 500,000 and 2,500,000.")

    return render(request, 'admins/riskuser.html', {'objv': obj})


def riskalert(request, tuser):
    obj = GiverTransaction.objects.get(id=tuser)
    
    if request.method == "POST":
        admin = request.POST.get('name')
        names = request.POST.get('name1')
        Sendquery.objects.create(transid=obj, sendquery=admin, name=names)

        # Blockchain-like smart contract interaction
        log_blockchain_action("Risk Alert Created", f"Risk alert created for transaction ID {obj.id} by admin {admin}. Alert sent to {names}.")

    return render(request, 'admins/riskalert.html')

