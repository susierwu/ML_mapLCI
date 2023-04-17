# functions for dataframe output once ML model done:
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

######################## finding a LCI process name only, no LCIA score calculated, for ecoinvent, USLCACommons databases ########
def map_single_lci (cosine_scores, product_list, mapdb_list):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    result_df = pd.DataFrame()
    for ix, product in enumerate(product_list):
        sorted_product_cs = sorted_cs[ix].cpu().numpy()
        naics_ix = indices[ix].cpu().numpy()
        result_df.loc[ix, 'your_product'] = product
        #naics_ix[0] gives you the index for the element with highest cos_score since it's descending:
        result_df.loc[ix, 'LCI_mapped'] = mapdb_list[naics_ix[0]]   
        result_df.loc[ix, 'cosine_score'] = float("{:.3f}".format(sorted_product_cs[0]))
    return(result_df)



def map_multiple_lci (cosine_scores, n, product_list, mapdb_list):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    result_df = pd.DataFrame()
    #n = 8
    prod_col = []
    eidb_col = []
    score_col = []
    for ix, product in enumerate(product_list):
        sorted_product_cs = sorted_cs[ix].cpu().numpy()
        naics_ix = indices[ix].cpu().numpy()
        prod_col.append([product] * n)
        eidb_col.append(mapdb_list[[naics_ix[i] for i in range(n)]]  )
        score_col.append([sorted_product_cs[i] for i in range(n)])  
    result_df["your_product"] = [y for x in prod_col for y in x] #flatten the list
    result_df["LCI_mapped"] = [y for x in eidb_col for y in x]
    result_df["ML_score"] = [y for x in score_col for y in x]
    result_df.index = list(range(1,n+1,1)) * len(product_list)  #this is the order of the ML score for each product
    result_df = result_df.set_index('your_product', append=True).swaplevel(0,1)
    return(result_df)
###############################################################################################################################



##### AGRIBALYSE_ready-to-eat_product, user can select multiple LCIA , final mapped LCI will have LCIA score shown together  ####

# return a list, each list contains LCIA scores for different life cycle stage, index[0]-[6] for each LC
def agribs_extract_lcia (dict_IC_unit, lcia_unit, sel_ic_multiple, agri_df):
    LC_lcia = []
    for sel_ic in sel_ic_multiple:
        sel_ic_i = list(dict_IC_unit.keys()).index(sel_ic)
        LC_Agriculture  = agri_df[(lcia_unit[sel_ic_i]),"Agriculture"].values   
        LC_Transformation = agri_df[(lcia_unit[sel_ic_i]),"Transformation"].values   
        LC_Pack  = agri_df[(lcia_unit[sel_ic_i]),"Emballage"].values   
        LC_Transport  = agri_df[(lcia_unit[sel_ic_i]),"Transport"].values   
        LC_Shop  = agri_df[(lcia_unit[sel_ic_i]),"Supermarché et distribution"].values   
        LC_Consume = agri_df[(lcia_unit[sel_ic_i]),"Consommation"].values   
        LC_Total  = agri_df[(lcia_unit[sel_ic_i]),"Total"].values
        LC_lcia.append([LC_Agriculture, LC_Transformation, LC_Pack, LC_Transport, LC_Shop, LC_Consume, LC_Total])
    return LC_lcia



def map_agribs_single_lci_wh_lcia (cosine_scores,dict_IC_unit, sel_ic_multiple, product_list, mapdb_list, LC_lcia):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    all_result = []
    
    for  i, sel_ic  in enumerate(sel_ic_multiple):
        ############# put result_df within each IC, then append to final all_result list
        result_df = pd.DataFrame()
        for ix, product in enumerate(product_list):
            sorted_product_cs = sorted_cs[ix].cpu().numpy()
            naics_ix = indices[ix].cpu().numpy()
            result_df.loc[ix, 'your product'] = product
            result_df.loc[ix, 'AGRIBALYSE_mapped'] = mapdb_list[naics_ix[0]]   
            result_df.loc[ix, dict_IC_unit.get(sel_ic)] = LC_lcia[i][6][naics_ix[0]]  #the [6] for total LCIA for each IC
            result_df.loc[ix, 'cosine_score'] = float("{:.3f}".format(sorted_product_cs[0]))
        all_result.append(result_df)
    return(all_result)



def map_agribs_multiple_lci_wh_lcia (n, cosine_scores,dict_IC_unit, sel_ic_multiple, product_list, mapdb_list, LC_lcia):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    final_result = []

    for i, sel_ic  in enumerate(sel_ic_multiple):
        prod_col ,database_col,score_col,total_col  = [], [], [], []
        agri_col,transformation_col, pack_col, trnspt_col,shop_col,consume_col = [], [], [], [], [], []
        result_df = pd.DataFrame()

        for ix, product in enumerate(product_list):
            sorted_product_cs = sorted_cs[ix].cpu().numpy()
            naics_ix = indices[ix].cpu().numpy()
            prod_col.append([product] * n)
            database_col.append(mapdb_list[[naics_ix[i] for i in range(n)]].tolist() )
            score_col.append([sorted_product_cs[i] for i in range(n)])  
            #################################################################################################
            total_col.append(LC_lcia[i][6][[naics_ix[i] for i in range(n)]].tolist())
            agri_col.append(LC_lcia[i][0][[naics_ix[i] for i in range(n)]].tolist())
            transformation_col.append(LC_lcia[i][1][[naics_ix[i] for i in range(n)]].tolist())
            pack_col.append(LC_lcia[i][2][[naics_ix[i] for i in range(n)]].tolist())
            trnspt_col.append(LC_lcia[i][3][[naics_ix[i] for i in range(n)]].tolist())
            shop_col.append(LC_lcia[i][4][[naics_ix[i] for i in range(n)]].tolist())
            consume_col.append(LC_lcia[i][5][[naics_ix[i] for i in range(n)]].tolist())

        result_df["your_product"] = [y for x in prod_col for y in x] #flatten the list
        result_df["AGRIBALYSE_mapped"] = [y for x in database_col for y in x]
        result_df["ML_score"] = [y for x in score_col for y in x]
        result_df["total"] = [y for x in total_col for y in x]
        result_df["agriculture"] = [y for x in agri_col for y in x]
        result_df["transformation"] = [y for x in transformation_col for y in x]
        result_df["pack"] = [y for x in pack_col for y in x]
        result_df["trnspt"] = [y for x in trnspt_col for y in x]
        result_df["shop"] = [y for x in shop_col for y in x]
        result_df["consume"] = [y for x in consume_col for y in x]
        result_df.index = list(range(1,n+1,1)) * len(product_list)  #this is the order of the ML score for each product
        result_df = result_df.set_index([ [sel_ic]*n*len(product_list),'your_product'], append=True).swaplevel(0,2)
        final_result.append(result_df)
    return(final_result)

###############################################################################################################################




####################### AGRIBALYSE_farm-gate_product, user can select multiple LCIA , final mapped LCI will have the final single farm-gate LCIA score shown together, major change from ready-to-eat product is that no diff. LC stage #####################

# need to add in another parameter all_lcia as its original col_name to screen DF, no need for lcia_unit parameter though
def agribs_farm_gate_extract_lcia (all_lcia, dict_IC_unit, sel_ic_multiple, agri_df):
    LC_lcia = []
    for sel_ic in sel_ic_multiple:
        sel_ic_i = list(dict_IC_unit.keys()).index(sel_ic)
        LC_Total  = agri_df[(all_lcia[sel_ic_i])].values
        LC_lcia.append(LC_Total)
    return LC_lcia


def map_agribs_farm_gate_single_lci_wh_lcia (cosine_scores,dict_IC_unit, sel_ic_multiple, product_list, mapdb_list, LC_lcia):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    all_result = []
    
    for  i, sel_ic  in enumerate(sel_ic_multiple):
        ############# put result_df within each IC, then append to final all_result list
        result_df = pd.DataFrame()
        for ix, product in enumerate(product_list):
            sorted_product_cs = sorted_cs[ix].cpu().numpy()
            naics_ix = indices[ix].cpu().numpy()
            result_df.loc[ix, 'your product'] = product
            result_df.loc[ix, 'AGRIBALYSE_mapped'] = mapdb_list[naics_ix[0]]   
            ############################. only one total LCIA for each IC -> LC_lcia[i] ############################
            result_df.loc[ix, dict_IC_unit.get(sel_ic)] = LC_lcia[i][naics_ix[0]]  
            result_df.loc[ix, 'cosine_score'] = float("{:.3f}".format(sorted_product_cs[0]))
        all_result.append(result_df)
    return(all_result)


def map_agribs_farm_gate_multiple_lci_wh_lcia (n, cosine_scores,dict_IC_unit, sel_ic_multiple, product_list, mapdb_list, LC_lcia):
    sorted_cs, indices = cosine_scores.sort(dim=1, descending=True)
    final_result = []

    for i, sel_ic  in enumerate(sel_ic_multiple):
        prod_col ,database_col,score_col,total_col  = [], [], [], []
        result_df = pd.DataFrame()

        for ix, product in enumerate(product_list):
            sorted_product_cs = sorted_cs[ix].cpu().numpy()
            naics_ix = indices[ix].cpu().numpy()
            prod_col.append([product] * n)
            database_col.append(mapdb_list[[naics_ix[i] for i in range(n)]].tolist() )
            score_col.append([sorted_product_cs[i] for i in range(n)])  
            ############################ change LC_lcia[i][6] to LC_lcia[i] here as only one final LCIA################
            total_col.append(LC_lcia[i][[naics_ix[i] for i in range(n)]].tolist())
            
        result_df["your_product"] = [y for x in prod_col for y in x] #flatten the list
        result_df["AGRIBALYSE_mapped"] = [y for x in database_col for y in x]
        result_df["ML_score"] = [y for x in score_col for y in x]
        result_df["farm-gate_total"] = [y for x in total_col for y in x]
        result_df.index = list(range(1,n+1,1)) * len(product_list)  #this is the order of the ML score for each product
        result_df = result_df.set_index([ [sel_ic]*n*len(product_list),'your_product'], append=True).swaplevel(0,2)
        final_result.append(result_df)

    return(final_result)

###############################################################################################################################
