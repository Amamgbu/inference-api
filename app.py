from flask import Flask,jsonify,request, render_template
import mwapi
import time
import bz2  # necessary for decompressing dump file into text format
import json

app = Flask(__name__)

# This should work but could be more efficient:
#
#   1) You're looping through the .json.bz2 file twice and there's overhead for that. You can rewrite this so you build the
#   country_integer_dict and integer_country_dict objects at the same time as you build the cleaned_dict.
#   I did this and it went from 40 to 25 seconds for starting up
#
#   2) For items without regions, that's actually somewhat of a mistake and you can skip those (the else clause)
#   They are items that had coordinates but couldn't be geolocated to a country and can be treated the same as articles w/o groundtruth
#
#   3) Now that this has gotten more complicated, we should probably move it to a function (and then just call the function after you define it)
#   You'll have to keep the INTEGER_COUNTRY_DICT and CLEANED_DICT instantiations outside of the function so they persist after loading in the data
#   But this will cleanup the objects you don't need after building CLEANED_DICT (mainly `unique` and `country_integer_dict`)

# Below I changed the style of variable names. I use ALL_CAPS when instantiating global variables -- i.e. objects that will be used inside other functions
# This applies to INTEGER_COUNTRY_DICT and CLEANED_DICT but not the others.
#On app start, process data and save as dict
with bz2.open("data/region_groundtruth_2020_11_29_aggregated_enwiki.json.bz2", "rt") as file:
    unique = list(set(region for item in file for region in json.loads(item)['region_list']))

    #Country to integer/Integer to countries dict
    country_integer_dict = {country:i for i, country in enumerate(unique)}
    INTEGER_COUNTRY_DICT = {i:country for i, country in enumerate(unique)}

CLEANED_DICT = {}
with bz2.open("data/region_groundtruth_2020_11_29_aggregated_enwiki.json.bz2", "rt") as file:
    for i,new_item in enumerate(file):
        data = json.loads(new_item)
        if len(data['region_list']) > 1:
            for i in range(len(data['region_list'])):
                data['region_list'][i] = country_integer_dict[data['region_list'][i]]
            CLEANED_DICT[data['item']] = tuple(data['region_list'])
        elif len(data['region_list']) == 1:
            CLEANED_DICT[data['item']] = country_integer_dict[data['region_list'][0]]
        else:
            CLEANED_DICT[data['item']] = ''

        if i%100000 == 0:
            print('{0} lines processed'.format(i))

# not a priority, but if you want to be able to pass URL parameters to pre-fill the form fields
# e.g., https://experimental-embeddings.toolforge.org/?lang=en&page_title=La_Pintana
# You can do this by passing them to index.html here and making some small changes to index.html
# You can see an example here where I enabled it for a different interface:
# https://github.com/geohci/list-building-interface/commit/540ee8e93d68077825ab2f9e0fede84aa576935a
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/get-summary',methods=['GET'])
def get_link_summary():
    '''
    This function merges the get_outlinks/get_inlinks and get_summary function together to get summary stats of article
    '''
    lang,title,error,threshold = validate_api_args()
    if error is not None:
        data = {'Error':error}
        return jsonify(data),404
    else:
        outlinks = get_outlinks(title,lang)
        inlinks = get_inlinks(title,lang) 
        outlink_summary = get_summary_stats(outlinks,threshold)
        inlink_summary = get_summary_stats(inlinks,threshold)
        data = {'article': 'https://{0}.wikipedia.org/wiki/{1}'.format(lang, title),
            'results':{
                'outlink_count':len(outlinks),
                'inlink_count':len(inlinks),
                'outlink_summary':outlink_summary,
                'inlink_summary':inlink_summary
                }
        }
        
        return jsonify(data)  


def validate_api_args():
    '''
    description: This function validates the argument to be used for summary stats
    output: error,title and language
    '''
    title = None
    lang = None
    threshold = 0.5
    error = None


    if request.args.get('title') and request.args.get('lang'):
        lang = request.args.get('lang')
        title = request.args.get('title')

        if title is None:
            error = 'no matching article for <a href="https://{0}.wikipedia.org/wiki/{1}">https://{0}.wikipedia.org/wiki/{1}</a>'.format(lang,title)
    else:
        error = 'missing language -- e.g., "en" for English -- and title -- e.g., "2005_World_Series" for <a href="https://en.wikipedia.org/wiki/2005_World_Series">https://en.wikipedia.org/wiki/2005_World_Series</a>'

    # Doesn't need to be changed yet but I think down the line we might want to break this into two separate parameters:
    # `min_link_count` and `min_link_prop`
    # This way you could do things like say that above_threshold is at least 2 links and >5% of links
    # Conveniently, this will also simplify a lot of the int vs. float logic you have to use to figure out what threshold is
    if 'threshold' in request.args:
        try:
            threshold = float(request.args['threshold'])
        except ValueError:
            # if can't parse threshold, should return an error
            error = "Error: threshold value provided not a float: {0}".format(request.args['threshold'])


    return lang,title,error,threshold


def get_outlinks(title,language,session=None):
    """
    Description: This is a function extracts outlinks based on their titles and language used
    input: 
        title - Contains a list of titles or individual title
        language - Contains language to be used e.g en
        session - Session of URL
    
    output:
        outlinks- Returns tuple containing qid, title and list of outlinks
    
    
    """
    #if title is not a list and not None, convert to list
    if type(title) != type('') and hasattr(title, "__iter__"):
        pass
    elif title is None:
        return None
    else:
        title = [title]
    
    #If there is no session set, set one
    if session is None:
        # I use all caps variable names when they are global, otherwise lowercase
        sitename = '{0}.wikipedia'.format(language.lower())
        test_label = 'Inference API Outreachy (mwapi)'
        contact_email = 'isaac@wikimedia.org'
        session = mwapi.Session('https://{0}.org'.format(sitename), user_agent='{0} -- {1}'.format(test_label, contact_email))
    
    
    #Initialize outlinks list
    outlinks = []
    
    params = {'action':'query',
          'generator':'links',
          'prop':'pageprops',
          'ppprop':'wikibase_item',
          'gpllimit':500,
          'redirects':'',
          'gplnamespace':0,
          'titles':'|'.join(title)}

    # we set this as low priority a while back because it wasn't working for you but you can make this code much cleaner by using mwapi's continuation parameter
    # specifically, just change to: results = session.get(params, continuation=True)
    # and then instead of it being a single dictionary, it's a generator of dictionaries
    # so you do something like:
    # for result in results:
    #  ...
    # and you don't need the additional logic around results.get(continue...
    result = session.get(params)
    #This is the initial title passed into argument
    old_title = title
    try:
        if result.get('continue',None) is None:
            for pid in result['query']['pages']:
                #If page is not missing, Get only articles
                if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                    #Get wikidata id
                    qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                        
                    if qid is not None:
                        #Get outlink title
                        outlink_title = result['query']['pages'][pid].get('title',None)
                        outlinks.append((qid,outlink_title))    
                
            return outlinks
        else:
            #Get initial results
            for pid in result['query']['pages']:
                if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                    #Get wikidata id
                    qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                    if qid is not None:
                        outlink_title = result['query']['pages'][pid].get('title',None)
                        outlinks.append((qid,outlink_title))
                
            #check for continue parameter
            check_continue = result.get('continue',None)
            
            #extract value to continue from
            while check_continue is not None:
                cont_val = result.get('continue').get('gplcontinue')
                params = {'action':'query',
                          'generator':'links',
                          'prop': 'pageprops',
                          'ppprop':'wikibase_item',
                          'gpllimit':500,
                          'gplcontinue':cont_val,
                          'titles':'|'.join(old_title),
                          'redirects':'',
                          'gplnamespace':0

                         }
                result = session.get(params)
                for pid in result['query']['pages']:
                    if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                        #Get wikidata id
                        qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                        
                        if qid is not None:
                            outlink_title = result['query']['pages'][pid].get('title',None)
                            outlinks.append((qid,outlink_title))
                    
            
                check_continue = result.get('continue',None)
            return outlinks
        
                        
    except:
        return None

def get_inlinks(title,language,session=None):
    """
    Description: This is a function extracts inlinks based on article's title and language used
    input: 
        title - Contains a list of titles or individual title
        language - Contains language to be used e.g en
        session - Session of URL
    
    output:
        inlinks- Returns tuple containing qid and title of inlinks
    
    
    """
    #if title is not a list and not None, convert to list
    if type(title) != type('') and hasattr(title, "__iter__"):
        pass
    elif title is None:
        return None
    else:
        title = [title]
    
    #If there is no session set, set one
    if session is None:
        # I use all caps variable names when they are global, otherwise lowercase
        sitename = '{0}.wikipedia'.format(language.lower())
        test_label = 'Inference API Outreachy (mwapi)'
        contact_email = 'isaac@wikimedia.org'
        session = mwapi.Session('https://{0}.org'.format(sitename), user_agent='{0} -- {1}'.format(test_label, contact_email))
    
    
    #Initialize inlinks list
    inlinks = []
    
    params = {'action':'query',
          'generator':'linkshere',
          'prop':'pageprops',
          'ppprop':'wikibase_item',
          'glhlimit':500,
          'redirects':'',
          'glhnamespace':0,
          'titles':'|'.join(title)}
    
    result = session.get(params)
    #This is the initial title passed into argument
    old_title = title
    # see comment in get_outlinks about mwapi and continuation
    try:
        if result.get('continue',None) is None:
            for pid in result['query']['pages']:
                #If page is not missing, Get only articles
                if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                    #Get wikidata id
                    qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                        
                    if qid is not None:
                        #Get outlink title
                        inlink_title = result['query']['pages'][pid].get('title',None)
                        inlinks.append((qid,inlink_title))    
                
            return inlinks
        else:
            #Get initial results
            for pid in result['query']['pages']:
                if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                    #Get wikidata id
                    qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                    if qid is not None:
                        inlink_title = result['query']['pages'][pid].get('title',None)
                        inlinks.append((qid,inlink_title))
                
            #check for continue parameter
            check_continue = result.get('continue',None)
            
            #extract value to continue from
            while check_continue is not None:
                cont_val = result.get('continue').get('glhcontinue')
                params = {'action':'query',
                          'generator':'linkshere',
                          'prop': 'pageprops',
                          'ppprop':'wikibase_item',
                          'glhlimit':500,
                          'glhcontinue':cont_val,
                          'titles':'|'.join(old_title),
                          'redirects':'',
                          'glhnamespace':0

                         }
                result = session.get(params)
                for pid in result['query']['pages']:
                    if result['query']['pages'][pid].get('ns') == 0 and 'missing' not in result['query']['pages'][pid]:
                        #Get wikidata id
                        qid = result['query']['pages'][pid].get('pageprops',{}).get('wikibase_item',None)
                        
                        if qid is not None:
                            inlink_title = result['query']['pages'][pid].get('title',None)
                            inlinks.append((qid,inlink_title))
                    
                    #Added a cap of 5000
                    if len(inlinks) > 5000:
                        inlinks = inlinks[:5000]
                        return inlinks
            
                check_continue = result.get('continue',None)
            return inlinks
        
                        
    except:
        return None

def get_summary_stats(list_of_links,threshold=0.5):
    '''
    description: This function gets basic summary stats of outlinks/inlinks and regions associated with them.
    input: Takes in a list of outlinks' qid. It comes in as a tuple containing qid and title
    output: returns a dict containing summary stats
    
    '''
    # TODO: some unused variables here that can be removed
    start_time = time.time()
    region_list = [] #List containing unique regions per outlink
    
    link_list = [] #List of outlink_dict
    
    final_dict = {}#Dict containing count of regions 
    
    summary_stats = {}
    percentage_dict = {}
    
    
    region_list = [INTEGER_COUNTRY_DICT.get(CLEANED_DICT.get(outlink_item[0])) for outlink_item in list_of_links if CLEANED_DICT.get(outlink_item[0])]
    
    link_list = [{outlink_item[1]: INTEGER_COUNTRY_DICT.get(CLEANED_DICT.get(outlink_item[0]))} for outlink_item in list_of_links if CLEANED_DICT.get(outlink_item[0])]
    #List of unique regions
    unique_region_list = []
    # would be nice to use more descriptive variable names than x and y when the variables are more than just super simple objects
    for y in region_list:
        if type(y) == type('') and y != '':
            unique_region_list.append(y)
        elif type(y) == ():
            for x in y:
                unique_region_list.append(x)
        else:
            continue
    
    unique_region_list = list(set(unique_region_list))
    
    #unique_region_list = list(set(x for y in region_list for x in y))
    
    #total number of outlinks
    link_total = len(list_of_links)
    #Loop through unique regions
    for region in unique_region_list:
        #Give region an initial value of 0
        final_dict[region] = 0
        #Loop through list of outlink dicts and take count of number of outlinks that contain a region
        
        for link in link_list:
            #Check if region occurs in an outlink and increment by 1
            if list(link.values())[0]:
                if region in list(link.values())[0]:
                    final_dict[region] = final_dict[region] + 1

        percentage_dict[region] = round(100 * final_dict[region]/link_total,2)

    # Not clear to me why there's a distinction between above_threshold and using max_val to identify the most-heavily linked region
    # What's the reason for the regions above the threshold not being treated as the "predicted" regions?
    max_val = max(final_dict.values(),default=0)    
    
    
    #Check if threshold is an integer, if not convert
    # I think maybe a typo here with the "and not None" clause?
    # You can probably clean this code up a bit by having first a set of clauses that convert the threshold into either float or int
    # You could even make that into a separate function if you'd like
    # And then having a second set of clauses that do the above_threshold / below_threshold determination
    # Right now links might also be neither above or below threshold
    # For example, if threshold is 5 links and a region has five links it is not >5 nor is it <5
    # One of those inequalities needs to be made inclusive (>= or <=) -- I'll leave that to you
    # But all possible situations should fit into either above_threshold or below_threshold (but not neither or both)
    if type(threshold) != int and not None and type(threshold) != float:
        #Check if threshold is a string float e.g "2.3" and convert to actual float
        if '.' in threshold:
            try:
                threshold = float(threshold)
                if threshold > 1:
                    threshold = int(threshold)
                    #Contains regions with frequency of occurence above set threshold
                    above_threshold = [k for k,v in final_dict.items() if v > threshold]

                    #Contains regions with frequency of occurence below set threshold
                    below_threshold = [k for k,v in final_dict.items() if v < threshold]
                else:
                    above_threshold = [k for k,v in final_dict.items() if v > threshold * link_total]
                    below_threshold = [k for k,v in final_dict.items() if v < threshold * link_total]
            except:
                error = "Threshold passed is not a number. Please input a number and try again."
                return error
                
        else:
            #Converts to integer, Throws error if threshold is not a number
            try:
                threshold = int(threshold)
                #Contains regions with frequency of occurence above set threshold
                above_threshold = [k for k,v in final_dict.items() if v > threshold]
                
                #Contains regions with frequency of occurence below set threshold
                below_threshold = [k for k,v in final_dict.items() if v < threshold]
                
            except:
                error = "Threshold passed is not a number. Please input a number and try again."
                return error
    elif type(threshold) == float:
        above_threshold = [k for k,v in final_dict.items() if v > threshold * link_total]
        below_threshold = [k for k,v in final_dict.items() if v < threshold * link_total]
        
    elif type(threshold) == int:
        #Contains regions with frequency of occurence above set threshold
        above_threshold = [k for k,v in final_dict.items() if v > threshold]
                
        #Contains regions with frequency of occurence below set threshold
        below_threshold = [k for k,v in final_dict.items() if v < threshold]
                
    else:
        error = "You have passed in an incorrect argument. Format should either be number or float"
        return error
        
            
        
    
    #Sort final dict and percentage dict by frequency
    final_dict = dict(sorted(final_dict.items(), key=lambda x: x[1], reverse=True))
    percentage_dict = dict(sorted(percentage_dict.items(), key=lambda x: x[1], reverse=True))
    # you could simplify this by never explicitly creating percentage_dict and just doing round(100 * x[1]/link_total,2) here
    link_summ_list = [{'region':x[0],'link-count':x[1],'percent-dist':y[1]} for x,y in zip(final_dict.items(),percentage_dict.items()) ]

    # I think just a typo here with the double assignment
    summary_stats = summary_stats = {
        'regions': unique_region_list,
        'unique-count': len(unique_region_list),
        'link-percent-count-dist': link_summ_list,
        'above-threshold':above_threshold,
        'below-threshold': below_threshold,
        'region-prediction':[k for k,v in final_dict.items() if v == max_val]


    }
    return summary_stats 

if __name__ == '__main__':
    app.run(debug=True)