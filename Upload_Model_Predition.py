# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 10:42:18 2019

@author: Jordan
"""
from rdkit import Chem
from rdkit.Chem import Descriptors, Crippen, Lipinski

import pandas as pd
from pandas import DataFrame

from sklearn.linear_model import LinearRegression, Lasso
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

class finger_printer:
            
    def __init__(self):
        #self.smiles = smiles
        #self.mol_smiles = Chem.MolFromSmiles(smiles)
        #self.mol_smarts = Chem.MolFromSmarts(smiles)
        self.aromatic_frac = Chem.MolFromSmarts('a')
        
      
    def arofrac(self,mol):
        matches = mol.GetSubstructMatches(self.aromatic_frac)
        num = mol.GetNumAtoms()
        aro_frac = len(matches)/num
        return(aro_frac)
        
    def descriptors(self, mol):
        aromatic_frac = self.arofrac(mol)
        mw = Descriptors.ExactMolWt(mol, False)
        valence_e = Descriptors.NumValenceElectrons(mol)
        h_acceptors = Lipinski.NumHAcceptors(mol)
        h_donors = Lipinski.NumHDonors(mol)
        NO_counts = Lipinski.NOCount(mol)
        NHOH_count = Lipinski.NHOHCount(mol)
        rotors = Lipinski.NumRotatableBonds(mol)
        SP3_frac = Lipinski.FractionCSP3(mol)
        logP = Crippen.MolLogP(mol)
        SP_bonds = len(mol.GetSubstructMatches(Chem.MolFromSmarts('[^1]')))
        return([aromatic_frac,mw,valence_e,h_acceptors,h_donors,NO_counts,NHOH_count, rotors,SP3_frac,logP,SP_bonds])


def write_new_dataframe():
    df = pd.read_csv('file:///C:/Users/Jordan/Documents/Citrine_Project/polymer_data_update.csv',encoding = "ISO-8859-1")
    new_FP_vec = []
    fp_er = finger_printer()
    for name, mol1,sol in df[['Polymer_Name','SMILES','Solubility_Parameter']].values:
        mol = Chem.MolFromSmiles(mol1)
        fp_new = fp_er.descriptors(mol)
        new_FP_vec.append([name,mol1,sol]+ fp_new)
    FP_DF = DataFrame(new_FP_vec)
    FP_DF.columns = ['Polymer_Name','SMILES','Solubility_Parameter','aromatic_frac'\
                     ,'mw','valence_e','h_acceptors','h_donors','NO_counts',\
                     'NHOH_count','rotors','SP3_frac','logP','SP_bonds']
    FP_DF.to_csv('final_data_set.csv')
    return(FP_DF) 

def split_data():
    data = write_new_dataframe()
    out_file = ['Polymer_Name','SMILES','Solubility_Parameter','Predicted_Solubility']
    features = ['Polymer_Name','SMILES','Solubility_Parameter','aromatic_frac','mw',\
                'valence_e','h_acceptors','h_donors','NO_counts','NHOH_count',\
                'rotors','SP3_frac','logP','SP_bonds']
    
    x = data.loc[:,features].values
    y = data.loc[:,'Solubility_Parameter'].values
    X_train, X_test, y_train, y_test = train_test_split(x,y, test_size=0.3)
    return(X_train,X_test,y_train,y_test,out_file)

def test_train_set():
    X_train,X_test,y_train,y_test,out_file = split_data()
    
    x_train = X_train[:,3:]
    x_test = X_test[:,3:]
    Xx_train = pd.DataFrame(X_train[:,:3])
    Xx_test = pd.DataFrame(X_test[:,:3]) 
    
    model = LinearRegression()
    reg = model.fit(x_train,y_train)
    
    reg_train_predictions = pd.DataFrame(reg.predict(x_train))
    reg_train_set = pd.concat([Xx_train,reg_train_predictions], axis=1)
    reg_train_set.columns = out_file
    reg_train_set.to_csv('linear_train_set.csv')
    
    reg_test_predictions = pd.DataFrame(reg.predict(x_test))
    reg_test_set = pd.concat([Xx_test,reg_test_predictions], axis=1)
    reg_test_set.columns = out_file
    reg_test_set.to_csv('linear_test_set.csv')
           
    x_train = StandardScaler().fit_transform(pd.DataFrame(X_train[:,3:]))
    out_train  = pd.DataFrame(X_train[:,:3])
    x_test  = StandardScaler().fit_transform(pd.DataFrame(X_test[:,3:]))
    out_test = pd.DataFrame(X_test[:,:3])
    
    pca = PCA(n_components=6)
    principalComponents_train = pca.fit_transform(x_train)
    principalComponents_test = pca.fit_transform(x_test)
    principalDf_train = pd.DataFrame(data = principalComponents_train
             , columns = ['principal component 1', 'principal component 2',
                          'principal component 3','principal component 4',
                          'principal component 5','principal component 6'])
    principalDf_test = pd.DataFrame(data = principalComponents_test
             , columns = ['principal component 1', 'principal component 2',
                          'principal component 3','principal component 4',
                          'principal component 5','principal component 6'])
    
    reg = model.fit(principalDf_train,y_train)
    
    train_predictions = pd.DataFrame(reg.predict(principalDf_train))
    pca_train_set = pd.concat([out_train,train_predictions], axis=1)
    pca_train_set.columns = out_file
    pca_train_set.to_csv('pca_train_set.csv')
    
    test_predictions = pd.DataFrame(reg.predict(principalDf_test))
    pca_test_set = pd.concat([out_test,test_predictions], axis=1)
    pca_test_set.columns = out_file
    pca_test_set.to_csv('pca_test_set.csv')
    
    model = Lasso(alpha=.1)
    lasso = model.fit(x_train,y_train)
    lasso_train_predictions = pd.DataFrame(lasso.predict(x_train))
    lasso_train_set = pd.concat([Xx_train,lasso_train_predictions], axis=1)
    lasso_train_set.columns = out_file
    lasso_train_set.to_csv('lasso_train_set.csv')
    
    lasso_test_predictions = pd.DataFrame(lasso.predict(x_test))
    lasso_test_set = pd.concat([Xx_test,lasso_test_predictions], axis=1)
    lasso_test_set.columns = out_file
    lasso_test_set.to_csv('lasso_test_set.csv')
      
    return(reg_train_set,reg_test_set,pca_test_set, pca_train_set,lasso_train_set,lasso_test_set)         
    
if __name__ == '__main__':
    self = 'a'
    test_train_set()
