from simplemediawiki import MediaWiki
from couchdb.client import Server
import uuid
import sys

def couch_connect():
    server = Server()
    try:
        db = server.create('feedme')
    except:
        db = server['feedme']
    return db

def save_recipe(db, recipe_doc):
    if ('Category:' not in recipe_doc['title']) and ('User:' not in recipe_doc['title']):
        recipe_doc['source'] = 'http://en.wikibooks.org/wiki/%s' % recipe_doc['title'].encode('ascii', 'replace')
        recipe_uuid = uuid.uuid5(uuid.NAMESPACE_URL, recipe_doc['source']).hex
        doc_exists = db.get(recipe_uuid)
        #print doc_exists, recipe_doc
        if not doc_exists:
            recipe_doc['type'] = 'recipe'
            recipe_doc['_id'] = recipe_uuid
            recipe_doc['title'] = recipe_doc['title'].replace('Cookbook:','').title()
            doc_id, doc_rev = db.save(recipe_doc)
            print "Added recipe %s (%s)" % (recipe_doc['title'], doc_id)
        else:
            print "Recipe %s already in database, skipping..." % recipe_doc['title']     

def list_recipes(db, wiki):
    try:
        recipes = wiki.call({'action': 'query', 'list': 'categorymembers', 'cmtitle': 'Category:Recipes', 'cmlimit': 'max'})
        #print recipes
        cmcontinue = recipes['query-continue']['categorymembers']['cmcontinue']
        for recipe in recipes['query']['categorymembers']:
            recipe_doc = recipe
            #print recipe_doc
            save_recipe(db, recipe_doc)
            
        while cmcontinue:
            recipes = wiki.call({'action': 'query', 'list': 'categorymembers', 'cmtitle': 'Category:Recipes', 'cmlimit': 'max', 'cmcontinue': cmcontinue})
            #print recipes
            if 'query-continue' in recipes:
                cmcontinue = recipes['query-continue']['categorymembers']['cmcontinue']
            else:
                cmcontinue = False
            for recipe in recipes['query']['categorymembers']:
                recipe_doc = recipe
                save_recipe(db, recipe_doc)
    
    except Exception:
        print "Unexpected error:", sys.exc_info()[0]
        print sys.exc_info()
        #print recipes
        

def fetch_recipes(db, wiki):
    try:
        recipes_without_content = db.view('feedme/recipes_without_text')
        for recipe in recipes_without_content:
            recipe_doc = recipe.value
            print recipe_doc
            recipe_content = wiki.call({'action': 'parse', 'pageid': recipe_doc['pageid']})['parse']
            for key in recipe_content:
                recipe_doc[key] = recipe_content[key]
            print recipe_doc
            db.save(recipe_doc)
    except Exception:
        print sys.exc_info()

def main():
    try:
        wiki = MediaWiki('http://en.wikibooks.org/w/api.php')
        my_db = couch_connect()
        list_recipes(my_db, wiki)
        fetch_recipes(my_db, wiki)
    except Exception:
        pass   
        
if __name__ == "__main__":
    main()