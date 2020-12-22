import csv
import sys
import jieba
import random
import re
from bert_slot_tokenizer import SlotConverter
vocab_path = '/share/nas165/Wendy/Study_202011/bert-slot-tokenizer/tests/test_data/example_vocab.txt' 
sc = SlotConverter(vocab_path, do_lower_case=True)
jieba.load_userdict('/share/nas165/Wendy/EZAIDialogue/Dataset/userDict.txt')

meal_set=['一號餐','1號餐','1號','A套餐','A號餐','二號餐','2號餐','2號','B套餐','B號餐','三號餐','3號餐','3號','C套餐','C號餐','四號餐','4號餐','4號','D套餐','D號餐','五號餐','5號餐','5號','F套餐','F號餐','六號餐','6號餐','6號','七號餐','7號餐','7號','八號餐','8號餐','8號','九號餐','9號餐','9號','十號餐','10號餐','10號','十一號餐','11號餐','11號','十二號餐','12號餐','12號','十三號餐','14號餐','14號','十四號餐','15號餐','15號','十五號餐','16號餐','16號','十六號餐','17號餐','17號','十七號餐','18號餐','18號','十八號餐','18號餐','十九號餐','19號餐','19號']
regex_meal_set=re.compile('.號餐') 
hito_meals=['花生豬排蛋吐司','培根三明治','薯條','鮪魚玉米夾蛋丹麥吐司','小薯餅','燒肉雞蛋丹麥吐司','司蛋餅','雞塊','餐包','招牌三明治','香濃起司營養三明治','花生薯餅蛋三明治','菜脯雞肉三明治','肉鬆蔥花起司三明治','特級培根三明治','里肌豬排三明治','香酥雙雞三明治','起司薯泥鮪魚蛋三明治','花生豬排培根蛋三明治','菜脯蔥蛋土司','香濃起司玉米蛋土司','薯泥火腿蛋土司','肉鬆薯泥土司','花生培根蛋土司','火腿薯餅蛋土司','雙倍香濃起司蛋土司','香蔥蛋椒盤燒肉土司','花枝炸物土司','薯泥沙拉蛋土司','黃瓜雞蛋三明治','DiDi卡三明治','丹麥鮮蔬薯泥','鮮蔬雞蛋堡','慢烤起司三明治','丹麥DiDi卡','火腿雞蛋堡','香酥雞肉堡','薯餅雞蛋堡','香蔥椒鹽燒肉堡','黃金炸豬起司堡','香辣雞腿肉蛋堡','脆皮雞腿堡','泰式辣味雞腿堡','花生醬起司牛肉堡','培根牛肉起司堡','豬肉丼刈包','牛肉丼刈包','黃金炸豬起司刈包','原味蛋餅','菜脯蔥蛋餅','火腿蛋餅','玉米蛋餅','起司蛋餅','泰式辣鬆蛋餅','特級培根蛋餅','黃金薯餅蛋餅','薯泥起司蛋餅','豬排蛋餅','沙茶拌麵','椒麻拌麵','沙茶燒肉拌麵','椒麻燒肉拌麵','豬肉丼拌麵','牛肉丼拌麵','烏龍湯麵','熱狗','四方薯餅','薯泥沙拉蛋','波浪薯條','蘿蔔糕','煎蛋蘿蔔糕','經典雞塊','甜不辣','地瓜黃金球','黃金脆薯','奶油餐包','雞肉棒','唐揚炸雞','特級培根義大利麵','花枝天婦羅義大利麵','培根雞肉義大利麵','脆皮雞腿義大利麵','黃金炸豬義大利麵','招牌咖啡','拿鐵咖啡','摩卡咖啡','古早味紅茶','伯爵紅茶','伯爵紅','手工冬瓜茶','茉香綠茶','豆漿','豆漿紅茶','柳橙汁','紅茶鮮奶','伯爵鮮奶','冬瓜鮮奶','綠茶鮮奶','豆漿鮮奶','巧克力鮮奶','鮮奶','咖啡拿鐵','培根蛋餅','鮮奶茶']
quantity=['一份','1份','*1','二份','2份','*2','三份','3份','*3','四份','4份','*4','五份','5份','*5','一個','1個','二個','2個','三個','3個','四個','4個','五份','5份','一杯','1杯','二杯','2杯','三杯','3杯','四杯','4杯','五杯','5杯']
regex_quantity=re.compile('.份') 
soup=['玉米濃湯','雞肉濃湯']
drink_temperature=['冰','熱','溫','冰的','熱的','溫的']
drink_sugar=['無糖','微糖','半糖','全糖']
drink_size=['大','中','小','大杯','中杯','小杯']
hito_meals_plus=['起司','丹麥','蛋','司']
meal_take=['外帶','內用','自取']
meal_package=['裝成一份','裝成一袋','分開裝','兩盒裝','裝一盒']
order_date=['明天','今天','早上','明早']
fp = open("Order_test.csv", "a")
fp2 = open("Order_more.csv", "a")

with open('/share/nas165/Wendy/Study_202011/bert-slot-tokenizer/Order2.csv', newline='', encoding = "Big5") as csvFile:
  rows = csv.DictReader(csvFile)
  for row in rows:
    slot={'meal_set':'空','hito_meals':'空','quantity':'1','drink':'空','soup':'空','drink_temperature':'空','drink_sugar':'微糖','drink_size':'小','hito_meals_plus':'空','meal_take':'空','meal_package':'空','order_date':'空','order_time':'空'}
    cutquery=jieba.lcut(row['問題'])
    query=row['問題']
    ls=[]
    for idx,q in enumerate(cutquery):
        if(q in meal_set or regex_meal_set.match(q)):
            for i in meal_set:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))        
            slot['meal_set']=q
        elif(q in hito_meals):
            for i in hito_meals:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))              
            slot['hito_meals']=q
        elif(q in quantity or regex_quantity.match(q)):
            for i in quantity:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))  
            slot['quantity']=q
            # if(q[0]=='一'):
            #     slot['quantity']=str(1)
            # elif(q[0]=='二' or q[0]=='兩'):
            #     slot['quantity']=str(2)
            # elif(q[0]=='三'):
            #     slot['quantity']=str(3)
            # elif(q[0]=='四'):
            #     slot['quantity']=str(4)
            # elif(q[0]=='五'):
            #     slot['quantity']=str(5) 
            # elif(q[0]=='*'):
            #     slot['quantity']=str(q[1])     
            # else:
            #     slot['quantity']=str(q[0])     
        elif(q in soup):
            for i in soup:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))  
            slot['soup']=q
        elif(q in drink_temperature):
            for i in drink_temperature:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery)) 
            slot['drink_temperature']=q
        elif(q in drink_sugar):
            for i in drink_sugar:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery)) 
            slot['drink_sugar']=q
        elif(q in drink_size):
            for i in drink_size:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery)) 
            slot['drink_size']=q[0]
        elif(q in hito_meals_plus):
            for i in hito_meals_plus:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))
            slot['hito_meals_plus']=q
        elif(q in meal_take):
            for i in meal_take:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))
            slot['meal_take']=q
        elif(q in order_date):
            for i in order_date:
                rcutquery=cutquery[:] #複製一份list
                rcutquery[cutquery.index(q)]=i
                ls.append("".join(rcutquery))
            slot['order_date']=q
        elif(q==':'):
            slot['order_time']="".join(cutquery[cutquery.index(':')-1:cutquery.index(':')+2])
    for idx,l in enumerate(ls):
        if(idx%10)==0:
            fp.write(str(l)+'\n')
        else:
            fp2.write(str(l)+'\n')
    # output_text, iob_slot = sc.convert2iob(query, slot)
    # for t,s in zip(output_text,iob_slot):
    #     fp.write(str(t)+' '+str(s)+'\n')
    # fp.write('\n')
fp.close()
fp2.close()