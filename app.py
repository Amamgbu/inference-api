from flask import Flask,jsonify,request, render_template
import pandas as pd
import mwapi
import bz2  # necessary for decompressing dump file into text format
import json

app = Flask(__name__)


#On app start, process data and saved as dict
cleaned_dict = {}
with bz2.open("data/region_groundtruth_2020_11_29_aggregated_enwiki.json.bz2", "rt") as file:
    for item in file:
        data = json.loads(item)
        cleaned_dict[data['item']] = data['region_list']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/v1/get-summary',methods=['GET'])
def get_outlink_summary():
    '''
    This function merges the get_outlinks and get_summary function together to get summary stats of article
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

    if 'threshold' in request.args:
        try:
            threshold = float(request.args['threshold'])
        except ValueError:
            threshold = "Error: threshold value provided not a float: {0}".format(request.args['threshold'])


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
        SITENAME = f'{language.lower()}.wikipedia'
        test_label = 'Inference API Outreachy (mwapi)'
        contact_email = 'isaac@wikimedia.org'
        session = mwapi.Session('https://{0}.org'.format(SITENAME), user_agent='{0} -- {1}'.format(test_label, contact_email))
    
    
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
        SITENAME = f'{language.lower()}.wikipedia'
        test_label = 'Inference API Outreachy (mwapi)'
        contact_email = 'isaac@wikimedia.org'
        session = mwapi.Session('https://{0}.org'.format(SITENAME), user_agent='{0} -- {1}'.format(test_label, contact_email))
    
    
    #Initialize outlinks list
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
    region_list = [] #List containing unique regions per outlink
    
    link_list = [] #List of outlink_dict
    
    final_dict = {}#Dict containing count of regions 
    
    summary_stats = {}
    percentage_dict = {}
    
    
    region_list = [cleaned_dict.get(outlink_item[0]) for outlink_item in list_of_links if cleaned_dict.get(outlink_item[0],None) is not None]
    
    link_list = [{outlink_item[1]: cleaned_dict.get(outlink_item[0])} for outlink_item in list_of_links if cleaned_dict.get(outlink_item[0],None) is not None]

    #List of unique regions
    unique_region_list = list(set(x for y in region_list for x in y))
    
    #total number of outlinks
    link_total = len(list_of_links)
    #Loop through unique regions
    for region in unique_region_list:
        #Give region an initial value of 0
        final_dict[region] = 0
        #Loop through list of outlink dicts and take count of number of outlinks that contain a region
        for link in link_list:
            #Check if region occurs in an outlink and increment by 1
            if region in list(link.values())[0]:
                final_dict[region] = final_dict[region] + 1

        percentage_dict[region] = round(100 * final_dict[region]/link_total,2)
    
    max_val = max(final_dict.values(),default=0)    
    
    
    #Check if threshold is an integer, if not convert
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
                above_threshold = [k for k,v in final_dict.items() if v >= threshold]
                
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
    link_summ_list = [{'region':x[0],'link-count':x[1],'percent-dist':y[1]} for x,y in zip(final_dict.items(),percentage_dict.items()) ]
    summary_stats = {
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

