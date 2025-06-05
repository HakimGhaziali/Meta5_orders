
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime
import time






class Meta:


    def __init__(self , symbol):
        self.authentication()
        self.symbol = symbol




    def authentication(self):
        if not mt5.initialize():
            print('this is error code', mt5.last_error())
            quit()


    def find_filling_mode(self):
    
        for i in range(2):
            request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": self.symbol,
            "volume": mt5.symbol_info(self.symbol).volume_min,
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(self.symbol).ask,
            "type_filling": i,
            "type_time": mt5.ORDER_TIME_GTC}

            result = mt5.order_check(request)
            
            if result.comment == "Done":
                break

        return i


    def sell_order_w(self , symbol ,lot ,comment ):
     
         price = mt5.symbol_info_tick(symbol).ask
         point = mt5.symbol_info(symbol).point
         filling_mode = self.find_filling_mode()

         request = {
             
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_SELL,
            "price": price,
            "deviation": 10,
            "magic": 0,
            "comment": comment,
            "type_filling": filling_mode,
            "type_time": mt5.ORDER_TIME_GTC}
         result = mt5.order_send(request)

         print(result)

         return result[2]

    def buy_order_w(self , symbol , lot , comment ):
         price = mt5.symbol_info_tick(symbol).ask
         filling_mode = self.find_filling_mode()

         request = {
             
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot,
            "type": mt5.ORDER_TYPE_BUY,
            "price": price,
            "deviation": 10,
            "magic": 0,
            "comment": comment,
            "type_filling": filling_mode,
            "type_time": mt5.ORDER_TIME_GTC}
         
         result = mt5.order_send(request)
         return result[2]
    
    def id_to_position(self , id_position):
        positions=mt5.positions_get(symbol= self.symbol)
        df=pd.DataFrame(list(positions),columns=positions[0]._asdict().keys())
        print(df)
        dt = df.query(f"ticket == {id_position}")
        print(dt)
        volume = dt['volume'].values
        comment = dt['comment'].values
        ticket = dt['ticket'].values
        
        data_dic = dict(symbol = self.symbol  , vol = volume[0] , comment = comment[0] , ticket = int(ticket[0]))


        return data_dic


    def close_buy_order(self ,  id_position ):
         filling_mode = self.find_filling_mode()
         data_dic = self.id_to_position(id_position)

         request = {
            "position": data_dic['ticket'],
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": data_dic['symbol'],
            "volume": data_dic['vol'],
            "type": mt5.ORDER_TYPE_SELL,
            "price": mt5.symbol_info_tick(data_dic['symbol']).bid,
            "deviation": 10,
            "magic": 0,
            "comment": data_dic['comment'],
            "type_filling": filling_mode,
            "type_time": mt5.ORDER_TIME_GTC}
         result = mt5.order_send(request)
         print(result)
         return result

    def close_sell_order(self , id_position):
         filling_mode = self.find_filling_mode()
         data_dic = self.id_to_position(id_position)

         request = {
            "position":data_dic['ticket'],
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": data_dic['symbol'],
            "volume": data_dic['vol'],
            "type": mt5.ORDER_TYPE_BUY,
            "price": mt5.symbol_info_tick(data_dic['symbol']).ask,
            "deviation": 10,
            "magic": 0,
            "comment": data_dic['comment'],
            "type_filling": filling_mode,
            "type_time": mt5.ORDER_TIME_GTC}
         result = mt5.order_send(request)
         print(result)
         return result
    



