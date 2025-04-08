# import json
# from typing import Dict, List
# from json import JSONEncoder
# import jsonpickle

# Time = int
# Symbol = str
# Product = str
# Position = int
# UserId = str
# ObservationValue = int


# class Listing:

#     def __init__(self, symbol: Symbol, product: Product, denomination: Product):
#         self.symbol = symbol
#         self.product = product
#         self.denomination = denomination
        
                 
# class ConversionObservation:

#     def __init__(self, bidPrice: float, askPrice: float, transportFees: float, exportTariff: float, importTariff: float, sugarPrice: float, sunlightIndex: float):
#         self.bidPrice = bidPrice
#         self.askPrice = askPrice
#         self.transportFees = transportFees
#         self.exportTariff = exportTariff
#         self.importTariff = importTariff
#         self.sugarPrice = sugarPrice
#         self.sunlightIndex = sunlightIndex
        

# class Observation:

#     def __init__(self, plainValueObservations: Dict[Product, ObservationValue], conversionObservations: Dict[Product, ConversionObservation]) -> None:
#         self.plainValueObservations = plainValueObservations
#         self.conversionObservations = conversionObservations
        
#     def __str__(self) -> str:
#         return "(plainValueObservations: " + jsonpickle.encode(self.plainValueObservations) + ", conversionObservations: " + jsonpickle.encode(self.conversionObservations) + ")"
     

# class Order:

#     def __init__(self, symbol: Symbol, price: int, quantity: int) -> None:
#         self.symbol = symbol
#         self.price = price
#         self.quantity = quantity

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + str(self.price) + ", " + str(self.quantity) + ")"
    

# class OrderDepth:

#     def __init__(self):
#         self.buy_orders: Dict[int, int] = {}
#         self.sell_orders: Dict[int, int] = {}


# class Trade:

#     def __init__(self, symbol: Symbol, price: int, quantity: int, buyer: UserId=None, seller: UserId=None, timestamp: int=0) -> None:
#         self.symbol = symbol
#         self.price: int = price
#         self.quantity: int = quantity
#         self.buyer = buyer
#         self.seller = seller
#         self.timestamp = timestamp

#     def __str__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"

#     def __repr__(self) -> str:
#         return "(" + self.symbol + ", " + self.buyer + " << " + self.seller + ", " + str(self.price) + ", " + str(self.quantity) + ", " + str(self.timestamp) + ")"


# class TradingState(object):

#     def __init__(self,
#                  traderData: str,
#                  timestamp: Time,
#                  listings: Dict[Symbol, Listing],
#                  order_depths: Dict[Symbol, OrderDepth],
#                  own_trades: Dict[Symbol, List[Trade]],
#                  market_trades: Dict[Symbol, List[Trade]],
#                  position: Dict[Product, Position],
#                  observations: Observation):
#         self.traderData = traderData
#         self.timestamp = timestamp
#         self.listings = listings
#         self.order_depths = order_depths
#         self.own_trades = own_trades
#         self.market_trades = market_trades
#         self.position = position
#         self.observations = observations
        
#     def toJSON(self):
#         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)

    
# class ProsperityEncoder(JSONEncoder):

#         def default(self, o):
#             return o.__dict__

from datamodel import OrderDepth, UserId, TradingState, Order
from typing import List, Dict
import string

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        """
        Only method required. It takes all buy and sell orders for all symbols as an input,
        and outputs a list of orders to be sent
        """
        # Initialize the method output dict as an empty dict
        result = {}

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():

                # Retrieve the Order Depth containing all the market BUY and SELL orders
                order_depth: OrderDepth = state.order_depths[product]

                sell_orders = list(order_depth.sell_orders.keys())
                sell_orders.sort()

                buy_orders = list(order_depth.buy_orders.keys())
                buy_orders.sort(reverse=True)

                # Initialize the list of Orders to be sent as an empty list
                orders: list[Order] = []

                # Note that this value of 1 is just a dummy value, you should likely change it!
                acceptable_price = 2020

                if product == "RAINFOREST_RESIN":
                    acceptable_price = 9997

                # If statement checks if there are any SELL orders in the market
                if len(order_depth.sell_orders) > 0:

                    # Sort all the available sell orders by their price,
                    # and select only the sell order with the lowest price
                    best_ask = sell_orders[0]
                    best_ask_volume = order_depth.sell_orders[best_ask]

                    if len(order_depth.sell_orders) > 1:

                        best_ask_2 = sell_orders[1]
                        best_ask_volume_2 = order_depth.sell_orders[best_ask_2]

                        if best_ask_2 < acceptable_price:
                            orders.append(Order(product, best_ask_2, -best_ask_volume_2))

                    # Check if the lowest ask (sell order) is lower than the above defined fair value
                    if best_ask < acceptable_price:

                        # In case the lowest ask is lower than our fair value,
                        # This presents an opportunity for us to buy cheaply
                        # The code below therefore sends a BUY order at the price level of the ask,
                        # with the same quantity
                        # We expect this order to trade with the sell order
                        print("BUY", str(-best_ask_volume) + "x", best_ask)
                        orders.append(Order(product, best_ask, -best_ask_volume))

                # The below code block is similar to the one above,
                # the difference is that it find the highest bid (buy order)
                # If the price of the order is higher than the fair value
                # This is an opportunity to sell at a premium
                if len(order_depth.buy_orders) != 0:
                    best_bid = buy_orders[0]
                    best_bid_volume = order_depth.buy_orders[best_bid]

                    if len(order_depth.buy_orders) > 1:
                        best_bid_2 = buy_orders[1]
                        best_bid_volume_2 = order_depth.buy_orders[best_bid_2]

                        if best_bid_2 > acceptable_price:
                            orders.append(Order(product, best_bid_2, -best_bid_volume_2))

                    if best_bid > acceptable_price:
                        print("SELL", str(best_bid_volume) + "x", best_bid)
                        orders.append(Order(product, best_bid, -best_bid_volume))

                # Add all the above the orders to the result dict
                result[product] = orders
                
        traderData = "" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 0

                # Return the dict of orders
                # These possibly contain buy or sell orders
                # Depending on the logic above
        
        return result, conversions, traderData
