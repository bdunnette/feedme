#!/usr/bin/python

from couchdb.client import Server
import urllib2
import json
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
        if not doc_exists:
            recipe_doc['type'] = 'recipe'
            recipe_doc['_id'] = recipe_uuid
            recipe_doc['title'] = recipe_doc['title'].replace('Cookbook:','').title()
            doc_id, doc_rev = db.save(recipe_doc)
            print "Added recipe %s (%s)" % (recipe_doc['title'], doc_id)
        else:
            print "Recipe %s already in database, skipping..." % recipe_doc['title']     

def list_recipes(db, api_url):
    try:
        recipe_query = '%s?format=json&action=query&list=categorymembers&cmtitle=Category:Recipes&cmlimit=max' % api_url
        recipes_json = urllib2.urlopen(recipe_query).read()
        recipes = json.loads(recipes_json)
        cmcontinue = recipes['query-continue']['categorymembers']['cmcontinue']
        print cmcontinue
        for recipe in recipes['query']['categorymembers']:
            recipe_doc = recipe
            save_recipe(db, recipe_doc)
            
        while cmcontinue:
            recipe_query = '%s?format=json&action=query&list=categorymembers&cmtitle=Category:Recipes&cmlimit=max&cmcontinue=%s' % (api_url, cmcontinue)
            recipes_json = urllib2.urlopen(recipe_query).read()
            recipes = json.loads(recipes_json)
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
        

def fetch_recipes(db, api_url):
    try:
        recipes_without_content = db.view('feedme/recipes_without_text')
        for recipe in recipes_without_content:
            recipe_doc = recipe.value
            recipe_query = '%s?action=parse&format=json&pageid=%s' % (api_url, recipe_doc['pageid'])
            recipe_json = urllib2.urlopen(recipe_query).read()
            recipe_content = json.loads(recipe_json)['parse']
            for key in recipe_content:
                recipe_doc[key] = recipe_content[key]
            print recipe_doc
            db.save(recipe_doc)
    except Exception:
        print sys.exc_info()
        
def fetch_images(db, api_url):
    try:
        images = db.view('feedme/images')
        for recipe in images:
            image_list = recipe.key
            image_files = recipe.value
            if image_files == None: 
                image_files = []
            if image_list and (len(image_list) != len(image_files)):
                print recipe
                recipe_doc = db.get(recipe.id)
                for image in image_list:
                    image_query = '%s?format=json&action=query&prop=imageinfo&titles=File:%s&iiprop=url|mime' % (api_url, image.encode('ascii', 'replace'))
                    image_info_json = urllib2.urlopen(image_query).read()
                    image_info_pages = json.loads(image_info_json)['query']['pages']
                    if '-1' in image_info_pages:
                        image_info = image_info_pages['-1']
                        if 'imageinfo' in image_info:
                            image_url = image_info['imageinfo'][0]['url']
                            print image_url
                            image_type = image_info['imageinfo'][0]['mime']
                            req = urllib2.Request(image_url, headers={'User-Agent': sys.argv[0]}) 
                            image_data = urllib2.urlopen(req).read()
                            db.put_attachment(recipe_doc, image_data, image, image_type)
    except Exception:
        print sys.exc_info()

def main():
    try:
        api_url = 'http://en.wikibooks.org/w/api.php'
        my_db = couch_connect()
        fetch_images(my_db, api_url)
        #list_recipes(my_db, api_url)
        #fetch_recipes(my_db, api_url)
        sys.exit(0)
    except Exception:
        pass   
        
if __name__ == "__main__":
    main()
