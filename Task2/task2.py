import time
from collections import deque

class TransactionMonitor:
    def __init__(self, threshold_amount, spike_multiple):
        self.threshold_amount = threshold_amount
        self.spike_multiple = spike_multiple
        self.transaction_window = deque()
        self.transaction_count = 0
        self.average_rate = 0

    def process_transaction(self, transaction_amount):
        timestamp = time.time()

        # Check for threshold alert
        if transaction_amount > self.threshold_amount:
            self.trigger_threshold_alert(transaction_amount)

        # Spike Alerting
        self.transaction_window.append((transaction_amount, timestamp))
        self.transaction_count += 1

        # Remove transactions outside the 1-hour window
        while self.transaction_window and timestamp - self.transaction_window[0][1] > 3600:
            self.transaction_count -= 1
            self.transaction_window.popleft()

        # Recalculate average rate. total number of transactions in transaction windows 
        # divided by timespan of those transaction. transaction window will have only last hours
        # transactions
        if not self.transaction_window or (timestamp - self.transaction_window[0][1]) == 0:
            self.average_rate = 0
        else:
            self.average_rate = self.transaction_count / (timestamp - self.transaction_window[0][1])

        # Check for a spike alert
        if self.transaction_count >= self.spike_multiple * self.average_rate:
            self.trigger_spike_alert(transaction_amount)

    def trigger_threshold_alert(self, transaction_amount):
        print(f"Threshold alert! Amount {transaction_amount} exceeded the predefined threshold.")

    def trigger_spike_alert(self, transaction_amount):
        print(f"Spike alert! Spike detected. Amount: {transaction_amount}")

# Create a TransactionMonitor instance with a threshold amount and spike multiple
monitor = TransactionMonitor(threshold_amount=1000, spike_multiple=10)

# Simulate a stream of transactions
transactions = [100, 800, 100, 100, 100, 200, 500, 1000, 700, 1100]

# Process each transaction
for transaction_amount in transactions:
    monitor.process_transaction(transaction_amount)