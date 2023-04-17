## Mapping product to current life cycle inventory (LCI) database with Machine Learning (ML)
 
adapting from "Amazon Science:Carbon assessment with machine learning": https://github.com/amazon-science/carbon-assessment-with-ml
 
Follow the installation instruction:
 
```
git clone https://github.com/amazon-science/carbon-assessment-with-ml.git
cd carbon-assessment-with-ml
pip install -r requirements.txt
pip install -e .
```
 
Currently available mapping database:
- ecoinvent database (EIDB): you can customize which version (cut-off, APOS, consequential) to map within the notebook (no impact score provided)
- Selected US Federal Commons LCI databases (no impact score provided), incl:
  - University of Washington Design for Environment Laboratory/Field Crop Production - 'UW_DfE_crop'
  - National Renewable Energy Laboratory/USLCI_2023_Q1_v1 - 'USLCI'
  - Federal Highway Administration/MTU Asphalt Pavement Framework - 'Hwy_pavement'
- AGRIBALYSE3.1: farm-gate as well as ready-to-eat food product, with user-selected impact categories (IC) LCIA scores extracted and plotted
