'''
Sample predictive model.
You must supply at least 4 methods:
- fit: trains the model.
- predict: uses the model to perform predictions.
- save: saves the model.
- load: reloads the model.
'''
import pickle
import numpy as np   # We recommend to use numpy arrays
from os.path import isfile

# You may want to use scikit-learn models, change to what suits you
# and make necessary changes wherever you spot "self.mod" in the code
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LinearRegression, LogisticRegression

class model:
    def __init__(self, verbose = True, use_scikit = False):
        '''
        This constructor is supposed to initialize data members.
        Use triple quotes for function documentation. 
        '''
        self.num_train_samples=0
        self.num_feat=1
        self.num_labels=1
        self.is_trained=False
        self.verbose = verbose
        self.mod = None
        if use_scikit:
        	self.mod = MultinomialNB() # This would work for a multi-class problem
        #	self.mod = LinearRegression() # This would work for a regression problem
        #	self.mod = LogisticRegression() # This would work for a two-class problem

    def fit(self, X, y):
        '''
        This function should train the model parameters.
        Here we do nothing in this example...
        Args:
            X: Training data matrix of dim num_train_samples * num_feat.
            y: Training label matrix of dim num_train_samples * num_labels.
        Both inputs are numpy arrays.
        For classification, labels could be either numbers 0, 1, ... c-1 for c classe
        or one-hot encoded vector of zeros, with a 1 at the kth position for class k.
        The AutoML format support on-hot encoding, which also works for multi-labels problems.
        Use data_converter.convert_to_num() to convert to the category number format.
        For regression, labels are continuous values.
        '''
        
        # Perform a few checks
        self.num_train_samples = X.shape[0]
        if X.ndim>1: self.num_feat = X.shape[1]
        num_train_samples = y.shape[0]
        if y.ndim>1: self.num_labels = y.shape[1]
        if self.verbose:        	
        	print("FIT: dim(X)= [{:d}, {:d}]").format(self.num_train_samples, self.num_feat)
        	print("FIT: dim(y)= [{:d}, {:d}]").format(num_train_samples, self.num_labels)        	
        assert(self.num_train_samples == num_train_samples)
        
        # Train a model "for real"
        if self.mod!=None:   
        	Y=y
            # For multi-class problems, convert target to be scikit-learn compatible
        	# into one column of a categorical variable. 
        	# For multi-label, regression of binary classification: do not convert.
        	Y=self.convert_to_num(y)  # Use this multi-class problems only
        	self.mod.fit(X, Y)
        	
        self.is_trained=True

    def predict(self, X):
        '''
        This function should provide predictions of labels on (test) data.
        Here we just return zeros...
        Make sure that the predicted values are in the correct format for the scoring
        metric. For example, binary classification problems often expect predictions
        in the form of a discriminant value (if the area under the ROC curve it the metric)
        rather that predictions of the class labels themselves. For multi-class or multi-labels
        problems, class probabilities are often expected if the metric is cross-entropy.
        Scikit-learn also has a function predict-proba, we do not require it.
        The function predict eventually can return probabilities.
        '''
        
        # Perform a few checks
        num_test_samples = X.shape[0]
        if X.ndim>1: num_feat = X.shape[1]
        if self.verbose: 
        	print("PREDICT: dim(X)= [{:d}, {:d}]").format(num_test_samples, num_feat)
        	print("PREDICT: dim(y)= [{:d}, {:d}]").format(num_test_samples, self.num_labels)
        assert(self.num_feat == num_feat)
        
        # Create empty predictions
        if self.num_labels>1:
        	y = np.zeros([num_test_samples, self.num_labels])
        else:
        	y = np.zeros(num_test_samples)
        
        # Make predictions for real	
        if self.mod!=None: 
        	y = self.mod.predict_proba(X) # Use this for multi-class or multi-label problems
        #	y = self.mod.predict_proba(X)[:,1] # Use this for two-class problems
        #	y = self.mod.predict(X) # Use this for regression
        
        return y

    def save(self, path="./"):
    	'''Dump model as pickle.'''
        pickle.dump(self, open(path + '_model.pickle', "w"))

    def load(self, path="./"):
    	'''Re-load previously saved model.'''
        modelfile = path + '_model.pickle'
        if isfile(modelfile):
            with open(modelfile) as f:
                self = pickle.load(f)
            	if self.verbose: print("Model reloaded from: " + modelfile)
        return self
        
    def convert_to_num(self, Ybin):
        ''' Convert binary targets to numeric vector (typically classification target values)'''
        if self.verbose: print("Converting to numeric vector")
        Ybin = np.array(Ybin)
        if len(Ybin.shape) ==1: return Ybin
        classid=range(Ybin.shape[1])
        Ycont = np.dot(Ybin, classid)
        if self.verbose: print Ycont
        return Ycont
