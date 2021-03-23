class SpatialModel:
    '''
    Description:
    
    This class holds all the model functions
    
    '''
    
    
    def __init__(self,groundtruth="region_groundtruth_2020_12_07_aggregated_frwiki.json.bz2",inlink_file="frwiki-inlinks-2020-12-sorted-v2.tsv.bz2",outlink_file="frwiki-outlinks-2020-12-sorted-v2.tsv.bz2",settings={'test_ratio':0.15,'threshold':0.2,'pass': 100,'iteration':5,'sample_size':None,'country-threshold-factor':{'United States':0.25}}):
        '''
        Description: 
        This contains the default values passed into the model
        
        Input parameters:
            - inlink_file: This is inlink file to be passed into model
            - outlink_file: This is outlink_file to be passed into model
            - test_ratio: This is ratio of test set to be used in train-test split
            - threshold: This is the threshold used in training model
            - pass: This is number of test set encountered before descriptive statistics is shown
            - iteration: This is the number of times model will be trained before predictions are done on test size
            - sample_size: The number of datasets to be used to create a baseline model
            - country-threshold-factor: Factor used to set relevance to countries
            
        '''
        self.inlink_file = inlink_file
        self.outlink_file = outlink_file
        self.groundtruth = groundtruth
        self.test_ratio = settings['test_ratio']
        self.threshold = settings['threshold']
        self.pass_rate = settings['pass']
        self.iteration = settings['iteration']
        self.sample_size = settings['sample_size']
        self.country_threshold_factor = settings['country-threshold-factor']
    
    def increase_field_size(self):
        
        maxInt = sys.maxsize
        #Increase field size

        while True:
            # decrease the maxInt value by factor 10 
            # as long as the OverflowError occurs.

            try:
                csv.field_size_limit(maxInt)
                break
            except OverflowError:
                maxInt = int(maxInt/10)
                
        message = 'Field size increased'
        return message
    
    
    def load_groundtruth(self,groundtruth=None):
        '''
        Description:
        This function takes in compressed groundtruth and returns a cleaned dictionary data.
        
        Input parameters:
            - groundtruth: This contains the groundtruth file
            
        Output:
            Returns a dictionary containing keys as QID/Article Page ID and values as regions 
        
        '''
        if not groundtruth:
            groundtruth = self.groundtruth
        
        self.cleaned_dict = {}
        
        with bz2.open(groundtruth, "rt") as file:
            tsvreader = csv.reader(file,delimiter='\t',quotechar='',quoting=csv.QUOTE_NONE)
            unique = list(set(region for item in tsvreader for region in item[2].split('|')))
            self.country_integer_dict = {country:i for i,country in enumerate(unique) }
            self.integer_country_dict = {i:country for i,country in enumerate(unique) }
    
            file.seek(0)

            for item in tsvreader:
                if item[0] == 'item':
                    continue
                else:
                    region_split = item[2].split('|') 
                    if len(region_split) > 1:
                        regions = []
                        for i in range(len(region_split)):
                            regions.append(self.country_integer_dict[region_split[i]])
                        self.cleaned_dict[item[0]] = tuple(regions)
                    elif len(region_split) == 1:
                        self.cleaned_dict[item[0]] = self.country_integer_dict[region_split[0]]
                    else:
                        continue
        
        return self.cleaned_dict,self.integer_country_dict,self.country_integer_dict
    
    
    
    
    def generate_statistics(self,country,initial_result,final_result):
        '''
        Description:
        
        Takes in both result lists and outputs a tuple containing TP,FP,FN,
        Recall,F1 score and Precision
        
        Input parameters:
            - country: Contains initial country dict
            - initial_result: Result generated from initial groundtruth
            - final_result: Result generated from final groundtruth
        
        
        Output:
            - Country dict containing keys as region and values as metrics for model evaluation calculation.
        
        
        '''
        
        for var in final_result:
            if country.get(var,None):
                continue
            else:
                country[var] = {'tp':0,'fp':0,'fn':0}

            if var in initial_result: 
                country[var]['tp'] += 1
            else:
                country[var]['fp'] += 1

        for var_sec in initial_result:
            if country.get(var_sec,None):
                continue
            else:
                country[var_sec] = {'tp':0,'fp':0,'fn':0}

            if var_sec not in final_result:
                country[var_sec]['fn'] += 1

        return country

    
    
    def clean_region_list(self,regions_list):
        '''
        Description:
        
        This function is used to remove all null values from region list passed in it. It also returns the number of regions
        
        Input parameters:
            - regions_list: List of regions 
            
        Output:
            - regions: Cleaned region list
            - link_total: Number of regions contained in list. This includes the null values
        
        '''
        
        
        
        regions = []
        link_total = len(regions_list)
        for region_item in regions_list:
            if region_item:
                if type(region_item) == str:
                    regions.append(region_item)
                else:
                    for region_item_ind in region_item:
                        regions.append(region_item_ind)
        return (regions,link_total) 

    
    def count_regions(self,cleaned_regions_list):
        '''
        Description:
        This function gets the region occurence
        
        Input parameters:
            - cleaned_region_list: List of all regions after cleaning is done.
        
        Output:
            - regions: Dictionary containing region occurence with keys being regions and values being region count.
        
        '''
        
        regions = {}
        for region in cleaned_regions_list:
            regions[region] = regions.get(region, 0) + 1
        return regions 
    
    def get_summary(self,link_total,regions_count_dict,threshold,threshold_factor):
        '''
        Description:
        This gets the regions within a specified threshold given an inlink/outlink
        
        Input parameters:
            - link_total: Total number of regions
            - regions_count_dict: Dictionary containing region occurence
            - threshold_factor: Factor used to set relevance to countries
            - threshold: This is the threshold set for links
        
        Output:
            - summarized: List containing regions that exist within the specified threshold
        
        
        
        '''
        summarized = []
        #Threshold/Threshold factor multiplication
        for k,v in regions_count_dict.items():
            if len(threshold_factor.keys()) > 0:
                if threshold_factor.get(k,None):
                    link_summary = link_total - (ceil(threshold_factor.get(k,None) * link_total))

                else:
                    link_summary = ceil(link_total * threshold)

                if v >= link_summary:
                    summarized.append(k)
            else:
                link_summary = ceil(link_total * threshold)

                if v >= link_summary:
                    summarized.append(k)


        return summarized

    def get_regions(self,qid,cleaned_dict,integer_country_dict):
        '''
        Description:
        Get regions associated with a QID/Article Page ID from groundtruth data.
        
        
        Input paramters:
            
            - qid: Wikipedia article Page ID/QID
            - cleaned_dict: initial groundtruth
            - integer_country_dict: Mapping of integers to countries
            
        Output:
            Returns tuple containing regions
        
        '''
        region_int = cleaned_dict.get(qid,None)
        if region_int:
            if isinstance(region_int,int):
                return integer_country_dict.get(region_int)
            else:
                region_int = list(region_int)
                for num in range(len(region_int)):
                    region_int[num] = integer_country_dict.get(region_int[num])
                return tuple(region_int)
        else:
            return None
        
    
    def save_groundtruth(self,cleaned_dict,name=None,path='.'):
        '''
        Description:
        This converts the saved dict into updated_groundtruth file
        
        Input parameters:
            - cleaned_dict: Updated groundtruth data
            - name of groundtruth
        '''
        try:
            if name:
                #Checks if file name exists in file directory
                all_path = [f for f in os.listdir(path) if f.startswith(name)]
                #Gets the number of occurence
                files_count = len(all_path)
                
                with bz2.open('{0}_{1}.json.bz2'.format(name,files_count+1),'wt') as file:
                    groundtruth_writer = csv.writer(file,delimiter='\t')
                    for item,item_val in cleaned_dict.items():
                        groundtruth_writer.writerow(json.dump({item:'|'.join(item_val)}))     
            else:
                name = 'updated_groundtruth'
                all_path = [f for f in os.listdir(path) if f.startswith(name)]
                
                files_count = len(all_path)
                with bz2.open('{0}_{1}.json.bz2'.format(name,files_count+1),'wt') as file:
                    groundtruth_writer = csv.writer(file,delimiter='\t')
                    for item,item_val in cleaned_dict.items():
                        groundtruth_writer.writerow(json.dump({item:'|'.join(item_val)}))

            message = "data successfully saved"
            logging.info(message)
            return file
        
        except Exception as e:
            return e
        
    def align_inlinks_outlinks(self,inlinks_reader,outlinks_reader):
        '''
        Description:
        This generator is used to align the inlinks and outlinks file based on page IDs/QIDs

        Input:
            - inlinks_reader: Opened inlink file
            - outlinks_reader: Opened outlink file

        Output:
            Tuple containing inlinks and outlinks

        '''


        inlinks = next(inlinks_reader)
        outlinks = next(outlinks_reader)
        while True:
            
            #Checks if both inlinks and outlinks can be iterated further
            if inlinks == float('-inf') and outlinks == float('-inf'):
                break
            elif inlinks == float('-inf'):
                inlinks = [float('-inf'),str(float('-inf'))]
            elif outlinks == float('-inf'):
                outlinks = [float('-inf'),str(float('-inf'))]
            else:
                pass
            
            if inlinks[1] == outlinks[1]:
                
                if inlinks[1] == 'article_qid' and outlinks[1] == 'article_qid':
                    inlinks = next(inlinks_reader)
                    outlinks = next(outlinks_reader)
                    
                else:
                    
                    if inlinks[0] == outlinks[0]:
                        yield (inlinks,outlinks)
                        try:
                            inlinks = next(inlinks_reader)
                            outlinks = next(outlinks_reader)
                        except StopIteration:
                            try:
                                outlinks = next(outlinks_reader)
                            except StopIteration:
                                break
                    else:
                        if inlinks[0] > outlinks[0]:
                            yield (None,outlinks)
                            try:
                                outlinks = next(outlinks_reader)
                            except StopIteration:
                                #Assign inifinitesimally small values when there is a Stop Iteration error
                                outlinks = float('-inf')
                        else:
                            yield (inlinks,None)
                            try:
                                inlinks = next(inlinks_reader)
                            except StopIteration:
                                inlinks = float('-inf')

            else:
                
                if inlinks[1] > outlinks[1]:
                    yield (None,outlinks)
                    try:
                        outlinks = next(outlinks_reader)
                    except StopIteration:
                        outlinks = float('-inf')
                else:
                    yield (inlinks,None)
                    try:
                        inlinks = next(inlinks_reader)
                    except StopIteration:
                        inlinks = float('-inf')
        
    def extract_region_summary(self,groundtruth,link,integer_country_dict,threshold,country_threshold_factor):
        '''
        Description:
            This is a helper function that brings other functions needed to get the region summary
            
        Input parameters:
            - groundtruth:
            - link: This is the inlink/outlink
            - integer_country_dict: This is the integer to country mapping to decode groundtruth
            
        Output:
            This returns a dict containing link summary
            
        
        '''
        #Split link(inlink/outlink)
        split_link = link[2].split(' ')

        #Get inlink region
        link_regions = [self.get_regions(item,groundtruth,integer_country_dict) for item in split_link]    

        #Clean regions
        cleaned_link_region_list,link_total = self.clean_region_list(link_regions)


        #Get region count
        link_region_count = self.count_regions(cleaned_link_region_list)
        
        #Get region summary
        link_regions_summary = self.get_summary(link_total,link_region_count,threshold,country_threshold_factor)

        
        return link_regions_summary
    
    
    
    
    def train_test_split(self,aligned_inlinks_outlinks,test_ratio=None,sample_size=None):
        '''
        Description:
            Given a specified test ratio, this splits the inlink and outlink file into training and test files
        
        Input parameters:
            - inlink_file: Compressed inlink file
            - outlink_file: Compressed outlink file
            - test_ratio: Takes in a test ratio which splits files according to it
        
        Output:
            - train_inlinks: Inlink training data
            - test_inlinks: Inlink test data
            - train_outlinks: Outlink training data
            - test_outlinks: Outlink test data
        
        '''
        print(self.test_ratio)
        if not test_ratio:
            test_ratio = self.test_ratio
                
        #Initialize train and test files
        train_inlink_file = bz2.open('train_inlink_file.tsv.bz2','wt')
        train_inlink_writer = csv.writer(train_inlink_file,delimiter='\t')
        
        test_inlink_file = bz2.open('test_inlink_file.tsv.bz2','wt')
        test_inlink_writer = csv.writer(test_inlink_file,delimiter='\t')
        
        
        train_outlink_file = bz2.open('train_outlink_file.tsv.bz2','wt')
        train_outlink_writer = csv.writer(train_outlink_file,delimiter='\t')
        
        test_outlink_file = bz2.open('test_outlink_file.tsv.bz2','wt')
        test_outlink_writer = csv.writer(test_outlink_file,delimiter='\t')
        
        
        #If sample size exists, set sample size else set as float(inf)
        if not sample_size:
            sample_size = float('inf')
        
        #Train ratio        
        train_ratio = 1 - test_ratio
        
        print(train_ratio)
        #Initialize count for inlinks/outlinks train and test
        inlinks_train_count = 0
        inlinks_test_count = 0
        outlinks_train_count = 0
        outlinks_test_count = 0
        
        i = 0
        
        #Iterate through inlinks and outlinks file
        while True:
            if i % 100000 == 0:
                logging.info('{0} lines processed'.format(i))
            i += 1
            
            if i == sample_size:
                break

            #Generate random number from 0 and 1
            random_num = round(random.uniform(0,1), 2)
            
            align_inlinks_outlinks = aligned_inlinks_outlinks
            
            try:
                inlinks,outlinks = next(align_inlinks_outlinks)
            except StopIteration:
                break
            
            #Check if train_ratio is greater than random number and append to test data
            if random_num <= train_ratio:
                if inlinks:
                    
                    train_inlink_writer.writerow(inlinks)
                    inlinks_train_count += 1
                if outlinks:
                    
                    train_outlink_writer.writerow(outlinks)
                    outlinks_train_count += 1
            else:
                if inlinks:
                    
                    test_inlink_writer.writerow(inlinks)
                    inlinks_test_count += 1
                    
                if outlinks:
                    
                    test_outlink_writer.writerow(outlinks)
                    outlinks_test_count += 1
            
        
        logging.info('Train data count: {0} \n'.format(inlinks_train_count + outlinks_train_count))
        logging.info('Test data count: {0} \n'.format(inlinks_test_count + outlinks_test_count))
        logging.info('Train-test split ratio: {0} \n'.format((inlinks_test_count + outlinks_test_count)/(inlinks_train_count + outlinks_train_count + inlinks_test_count + outlinks_test_count )))
        
        #Close files
        train_inlink_file.close()
        test_inlink_file.close()
        train_outlink_file.close()
        test_outlink_file.close()
        
        return train_inlink_file,test_inlink_file,train_outlink_file,test_outlink_file
        
        
        
        
    def build_model(self,aligned_inlinks_outlinks_train,cleaned_dict,integer_country_dict,country_integer_dict,threshold=None,country_threshold_factor=None):
        '''
        Description: 
        This function is primarily used in training the model
        
        Input parameters:
            - train_inlinks: Inlink training data
            - train_outlinks: Outlink training data
        
        
        Output:
            Returns updated groundtruth
        
        
        
        '''
        if not cleaned_dict:
            cleaned_dict = self.cleaned_dict
        
        if not threshold:
            threshold = self.threshold
            
        if not country_threshold_factor:
            country_threshold_factor = self.country_threshold_factor
            
        
            
        inlinks,outlinks = next(aligned_inlinks_outlinks_train)
        

        while True:
            
            #Split inlinks
            if inlinks:
                #Get inlink region summary
                inlink_regions_summary = self.extract_region_summary(cleaned_dict,inlinks,integer_country_dict,threshold,country_threshold_factor)


                if len(inlink_regions_summary) > 0:
                    # Update groundtruth for inlink
                    cleaned_dict[inlinks[0]] = [ country_integer_dict.get(inlink_pred) for inlink_pred in inlink_regions_summary]
                    
            if outlinks:
                
                #Get outlink region summary
                outlink_regions_summary = self.extract_region_summary(cleaned_dict,outlinks,integer_country_dict,threshold,country_threshold_factor)


                if len(outlink_regions_summary) > 0:
                    # Update groundtruth for outlink
                    cleaned_dict[outlinks[0]] = [ country_integer_dict.get(outlink_pred) for outlink_pred in outlink_regions_summary]

            try:
                inlinks,outlinks = next(aligned_inlinks_outlinks_train)
            except StopIteration:
                break
            


        #Convert dictionary and save groundtruth
        save = self.save_groundtruth(cleaned_dict)
        logging.info('Model successfully saved')
        
        updated_groundtruth = cleaned_dict
        return updated_groundtruth
    
    
    def evaluate_model(self,country,cleaned_dict,integer_country_dict,country_integer_dict,aligned_inlinks_outlinks_train,aligned_inlinks_outlinks_test,threshold=None,country_threshold_factor=None,pass_rate=None):
        '''
        Description:
        This evaluates the model algorithm built.
        
        Input parameters:
        
            - cleaned_dict: Initial cleaned groundtruth dictionary
            - test_data_inlinks: Inlink test data
            - test_data_outlinks: Outlink test data
            - pass_rate: Number of passes made
            - iteration: Number of iterations made by model
            
        
        Output:
            Returns the summary stats
        
        
        '''
        if not pass_rate:
            pass_rate = self.pass_rate
        
        if not threshold:
            threshold = self.threshold
            
        if not country_threshold_factor:
            country_threshold_factor = self.country_threshold_factor
            
        
        #Train model
        updated_model_groundtruth_dict = self.build_model(aligned_inlinks_outlinks_train,cleaned_dict,integer_country_dict,country_integer_dict)

        #Align test set
        inlinks,outlinks = next(aligned_inlinks_outlinks_test)

        #If pass rate exists
        if pass_rate:
            #Loop through get evaluation statistics at every pass.Note that pass should not be greater than test size

            #Initialize a counter
            i = 0

            while True:
                if inlinks:
                    #Get initial inlink summary
                    initial_inlink_summary = self.extract_region_summary(cleaned_dict,inlinks,integer_country_dict,threshold,country_threshold_factor)

                    #Get final inlink summary from updated groundtruth
                    final_inlink_summary = self.extract_region_summary(updated_model_groundtruth_dict,inlinks,integer_country_dict,threshold,country_threshold_factor)

                    #Get comparison statistics
                    get_statistics = self.generate_statistics(country,initial_inlink_summary,final_inlink_summary)
                
                if outlinks:
                    #Get initial outlink summary
                    initial_outlink_summary = self.extract_region_summary(cleaned_dict,outlinks,integer_country_dict,threshold,country_threshold_factor)


                    #Get final inlink summary from updated groundtruth
                    final_outlink_summary = self.extract_region_summary(updated_model_groundtruth_dict,outlinks,integer_country_dict,threshold,country_threshold_factor)


                    #Get comparison statistics
                    get_statistics = self.generate_statistics(country,initial_outlink_summary,final_outlink_summary)



                if i % pass_rate == 0:
                    logging.info('--------------MODEL EVALUATION REPORT-------------- \n')

                    for country_key,country_val in country.items():
                        logging.info('{0}: \n'.format(country_key))


                        logging.info('TP: {0}, TN:{1}, FN:{2} \n'.format(country_val['tp'],country_val['fp'],country_val['fn']))

                        #Calculate Micro precision: (TP1 + TP2 +.... + TPN) / (TP1 +TP2 +.....+ TPN) + (FP1 +FP2 +....+ FPN)
                        micro_precision = country_val['tp']/(country_val['tp'] + country_val['fp'])
                        #self.precision_total += micro_precision

                        micro_recall = country_val['tp']/(country_val['tp'] + country_val['fn'])
                        #self.recall_total += self.micro_recall

                        micro_f1_score = 2 * (micro_precision*micro_recall)/(micro_precision + micro_recall)

                        logging.info('Precision: {0}, Recall:{1}, f1 score:{2} \n'.format(micro_precision,micro_recall,micro_f1_score))

                i += 1
                try:
                    inlinks,outlinks = next(align_inlinks_outlinks_test)
                except StopIteration:
                    break