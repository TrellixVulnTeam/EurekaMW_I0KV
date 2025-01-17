
import traceback

from com.eurekamw_mg.utils import SearchUtils as su, WordUtils as wu
from com.eurekamw_mg.db import DBUtils as dbu, DBConstant as DC
from com.eurekamw_mg.model import JSONCostants as JC

def generate_list(words):
    # Create a list from the input by splitting based on comma and trimming the whitespaces
    wordList = []
    for word in words.split(','):
        word=word.strip().lower()
        if(len(word)>0):
            wordList.append(word)
    #return the wordlist
    return wordList


def add_words_to_list(list_name, word_list):
    try:
        in_valid_word_list=[]
        for word in word_list:
            is_valid = su.search(word)
            if not is_valid:
               in_valid_word_list.append(word)
               word_list.remove(word)

        if len(in_valid_word_list) > 0:
            print('Unable to find following words: {0}'.format(in_valid_word_list))

        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        list_update_query={}
        list_update_query[JC.NAME] = list_name

        set_query = {}
        set_query[JC.PUSH] = {JC.LIST: {JC.EACH: word_list}}

        list_coll.update_one(list_update_query,set_query)
    except:
        traceback.print_exc()
    finally:
        client.close()


def remove_words_from_list(list_name, word_list):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        list_update_query={}
        list_update_query[JC.NAME] = list_name

        set_query = {}
        set_query[JC.PULL] = {JC.LIST: {JC.IN : word_list}}

        list_coll.update_one(list_update_query,set_query)
    except:
        traceback.print_exc()
    finally:
        client.close()

def sanatize_List(list):
    # Create a list from the input by splitting based on comma and trimming the whitespaces
    wordList = [word.strip().lower() for word in list]
    # return the wordlist
    return wordList

def get_list_names(listname):
    try:
        word_list = []

        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        list_create_query = {}
        list_create_query[JC.NAME] = listname

        results = list_coll.find(list_create_query)

        if results[0] is not None:
            for cat in results[0][JC.LIST]:
                for word in results[0][JC.LIST][cat]:
                    word_list.append(word[JC.NAME])
            # word_list = results[0][JC.LIST]
        return word_list
    except:
        traceback.print_exc()
    finally:
        client.close()

def get_compl_list(namelist):
    # namelist=get_list_names(listname)
    complete_list={}
    # complete_list[JC.NAME]=listname

    rlist={}
    for name in namelist:
        cat=wu.get_category(name)
        if cat is None:
            cat='None'
        if cat in rlist:
            # rlist[cat].append({name:su.get_selected_word_from_db(name,[JC.SHORTDEF])})
            rlist[cat].append({JC.NAME: name,JC.SHORTDEF:su.get_selected_word_from_db(name, [JC.SHORTDEF])[JC.SHORTDEF]})
        else:
            # rlist[cat]=[{name:su.get_selected_word_from_db(name,[JC.SHORTDEF])}]
            rlist[cat] = [{JC.NAME: name, JC.SHORTDEF:su.get_selected_word_from_db(name, [JC.SHORTDEF])[JC.SHORTDEF]}]
    # complete_list[JC.LIST]=rlist[JC.LIST]
    return rlist

def create(name, list):
    try:
        in_valid_word_list = []
        for word in list:
            is_valid = su.search(word)
            if not is_valid:
                in_valid_word_list.append(word)
                list.remove(word)

        if len(in_valid_word_list) > 0:
            print('Unable to find following words: {0}'.format(in_valid_word_list))

        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        list_create_query = {}
        list_create_query[JC.NAME] = name
        list_create_query[JC.LIST] = get_compl_list(list)

        list_coll.insert_one(list_create_query)
        return True
    except:
        traceback.print_exc()
        return False
    finally:
        client.close()

def get_lists():
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]

        list_coll = db[DC.LISTS_COLL]
        list = []
        result = list_coll.find()
        if result is not None:
            for cat in result:
                list.append(cat[JC.NAME])
            return list
            return []
    except Exception as exception:
        traceback.print_exc()
        return False
    finally:
        client.close()

def is_list_present(list_name):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        list_search_query={}
        list_search_query[JC.NAME] = list_name

        result = list_coll.count_documents(list_search_query)
        if result == 0:
            return False

        return True
    except:
        traceback.print_exc()
    finally:
        client.close()

def delete_list(list_name):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]
        list_coll = db[DC.LISTS_COLL]

        delete_query={}
        delete_query[JC.NAME] = list_name

        list_coll.delete_one(delete_query)
    except:
        traceback.print_exc()
    finally:
        client.close()

def update_list(list_name, new_list_name, new_word_list):
    if not is_list_present(list_name):
        print("No list with name '{0}' is present in DB.".format(list_name))
        return False

    if list_name != new_list_name and is_list_present(new_list_name):
        print("List with name '{0}' is already present in DB.".format(new_list_name))
        return False

    try:
        in_valid_word_list=[]
        for word in new_word_list:
            is_valid = su.search(word)
            if not is_valid:
               in_valid_word_list.append(word)
               new_word_list.remove(word)

        if len(in_valid_word_list) > 0:
            print('Unable to find following words: {0}'.format(in_valid_word_list))

        client = dbu.get_client()

        db = client[DC.DB_NAME]
        category_coll = db[DC.LISTS_COLL]

        category_update_query={}
        category_update_query[JC.NAME] = list_name

        new_data = {}
        # new_data[JC.PUSH] = {JC.LIST: {JC.EACH: word_list}}
        new_data[JC.NAME] = new_list_name
        new_data[JC.LIST] = get_compl_list(new_word_list)

        set_query={}
        set_query[JC.SET] = new_data

        check_query = {}
        check_query[JC.UPSERT] = 'True'
        category_coll.update_one(category_update_query, set_query)
        return True
    except:
        traceback.print_exc()
        return False
    finally:
        client.close()


# l=generate_list('testlist,,cat,ku.,,hh,,jjj,kkk')

# print(l)
# lt=['abate','abash','chagrin']
# create('testlist1',lt)
# print(get_lists())


# l=['dictum', 'bode', 'assent']
# update_list('testlist1', 'testlist1', l)

def get_list(listname):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]

        words_schema = db[DC.LISTS_COLL]
        search_data = {}
        search_data[JC.NAME] = listname
        if words_schema.count_documents(search_data) == 0:
            return None
        result = words_schema.find(search_data)
        print(result[0])
        return result[0]
    except Exception as exception:
        traceback.print_exc()
        return None
    finally:
        client.close()

def get_refesh_list(wordlist,cat_name):
    try:
        client = dbu.get_client()

        db = client[DC.DB_NAME]

        list_coll = db[DC.LISTS_COLL]
        list = set()
        search_query={}
        inner_search_query={}
        inner_search_query[JC.IN]=wordlist
        search_query['list.'+cat_name+'.name']=inner_search_query

        fetch_query={}
        fetch_query[JC.NAME]=1
        fetch_query[JC.ID]=0

        results = list_coll.find(search_query,fetch_query)
        for result in results:
            list.add(result[JC.NAME])
        if list is not None:
            return list
        return []
    except Exception as exception:
        traceback.print_exc()
        return False
    finally:
        client.close()

def refesh(listname):
    list = get_list_names(listname)
    update_list(listname, listname, list)

# print(cu.get)