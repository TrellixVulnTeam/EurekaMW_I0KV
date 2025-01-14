import os
import traceback

from flask import url_for

from com.eurekamw_mg.utils import SearchUtils as su
from com.eurekamw_mg.db import DBUtils as dbu, DBConstant as DC
from com.eurekamw_mg.model import JSONCostants as JC

def is_valid_word(wordname):
    word = su.search(wordname)
    if word is None:
        return False
    return True
#
# def update_category(wordname, category_name=''):
#     try:
#         client = dbu.get_client()
#
#         db = client[DC.DB_NAME]
#
#         words_schema = db[DC.WORDS_COLL]
#         search_query = {}
#         search_query[JC.ID] = wordname
#
#         new_values = {}
#         new_values[JC.CATEGORY] = category_name
#
#         set_query={}
#         set_query[JC.SET] = new_values
#         result = words_schema.update_one(search_query,set_query)
#         print(result.modified_count)
#         if result.modified_count is not 0:
#             return True
#         return False
#     except Exception as exception:
#         traceback.print_exc()
#         return False
#     finally:
#         client.close()

# print(update_category('charm','magical charms'))

def get_category(wordname):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]

        cat_coll = db[DC.CATEGORY_COLL]
        search_data = {}
        search_data[JC.LIST] = wordname
        if cat_coll.count_documents(search_data) == 0:
            return None
        result = cat_coll.find(search_data)
        return result[0][JC.NAME]
    except Exception as exception:
        traceback.print_exc()
        return None
    finally:
        client.close()

def load_words():
    with open(os.path.abspath('.')+'/static/utils/words_alpha.txt') as word_file:
        valid_words = set(word_file.read().split())

    return valid_words

def validate_wordlist(list):
    vaild_list=[]
    invaild_list=[]
    english_words = load_words()
    for word in list:
        if word in english_words:
            vaild_list.append(word)
        else:
            invaild_list.append(word)

    return {JC.VALID_LIST:vaild_list,JC.INVALID_LIST:invaild_list}