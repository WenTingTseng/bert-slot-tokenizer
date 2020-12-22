from bert_slot_tokenizer import SlotConverter
vocab_path = '/share/nas165/Wendy/Study_202011/bert-slot-tokenizer/tests/test_data/example_vocab.txt' 
# you can find a example here --> https://github.com/DevRoss/bert-slot-tokenizer/blob/master/tests/test_data/example_vocab.txt
sc = SlotConverter(vocab_path, do_lower_case=True)
text = '我要買1號餐2份'
slot={'meal_set':'1號餐','quantity':'2','drink_temperature':'空'}
#slot = {'meal_set': '1號餐','meal_set': '9號餐', 'quantity': '2份', 'quantity': '3份'}
output_text, iob_slot = sc.convert2iob(text, slot)
print(output_text)
# ['too', 'young', ',', 'too', 'simple', ',', 'some', '##times', 'na', '##ive', '!', '蛤', '蛤', '+', '1', '##s']
print(iob_slot)
# ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-name', 'I-name', 'B-time', 'I-time', 'I-time']