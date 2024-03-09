import json

import bookStack_pb2

json_data = '''
{
   "bookdata":[
      {
         "bookname":"图书1",
         "author":"zhangsan",
         "bookdescri":"这是zhangsan图书介绍",
         "imgbs64": "/aag/agaqfgg",
         "id": "afwqfq"
      },
      {
         "bookname":"图书2",
         "author":"zhann",
         "bookdescri":"这是zhann介绍",
         "imgbs64": "/aag/agag",
         "id": "afafgfq"
      }
   ],
   "category":{
      "0":{"分类1":["afagefa","rhrbah","aefaghhth"]},
      "1":{"分类2":["afafda","rhrvzah","aehhthrh"]},
      "2":{"分类3":["afa啊fa","rhrvhh","aehhthafa"]}
   },
   "mpage":20
}
'''

data = json.loads(json_data)
message = bookStack_pb2.MyData()

for item in data['bookdata']:
    new_book = message.bookdata.add()
    new_book.id = item['id']
    new_book.author = item['author']
    new_book.bookname = item['bookname']
    new_book.bookdescri = item['bookdescri']
    new_book.bookimgbs64 = item['imgbs64']

# for category_key, category_value in data['category'].items():
#     new_category = message.category.category_map.add()
#     new_category.key = category_key
#     for catename, catelist in category_value.items():
#         new_categoryList = new_category.category_items.category_list.add()
#         new_categoryList.catekey = catename
#         new_categoryList.values.extend(catelist)
#
# message.mpage = data['mpage']

serialized_data = message.SerializeToString()
print(serialized_data)

message.ParseFromString(serialized_data)
bookdata = message.bookdata
category = message.category
# mpage = message.mpage
print(bookdata[0])
print('category', category)
# print(mpage)
