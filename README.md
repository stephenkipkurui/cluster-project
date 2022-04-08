README.md

# ZILLOW PROJECT 

## Project Goals and Description: 

Zillow Group, Inc is an American Online Real-estate Marketplace Company Housing Company founded in 2004 in Seattle, WA. The company solely capitalize on online digital market through its website- https://www.zillow.com/. Through this portal, zillow continually collects millions and millions of data-points are captured about its customers each and every day. These information is analyzed by experts in Data Science and meaningful inferrence deducted.

This project is an example of on of the many studies on these collected data. Our goal however, will be focused on understanding the z-estimate error in the 2017 data for single household homes in three Carlifonia Counties- Orange, L.A. and Ventura. We will construct an additional new machine learning models as a continuation to the regression model created in the end month of March, 2022 to complement the current one in production with the ultimate purpose of predicting key drivers for Z-estimate errors (Log Errors) values for single family properties. The approach here is implementation of clustering concepts in exploration and visualization of data.

## Initial Hypothesis/Questions
Questions this project aims to answe:
- Q1. Does the size of __land (lot size)__ affect the errors in z-estimate?
- Q2. Does the __home square feet__ of homes affect z-estimate?
- Q3. Controlling __location (counties)__, how is the z-estimate affected?
- Q4. Controlling __tax value__, how is the z-estimate affected?
- Q5. Lastly how are the __age of the homes__ in counties affect z-estimates counties?
- Q6. How are the means average sizes of land and home square feet in different counties affect z-estimate.


## The Project Plan Structure 

This projects follows Data Science Pipeline. Should you wish to recreate the project, follow the following general steps:

# (i). Planning 
>- Define goals, understand the stakeholders and or audience, brain-storm to arrive at the MVP, define end product and purpose. Finally deliver report through presentation.


# (ii). Acquisition

>- Create a connection with CodeUp Online SQL through conn.py module.
>- Call the conn.py function with the acquire.py function.
>- Save a cached copy of the .csv file in local machine.
>- Import this module and other required python libraries into the main zillow_workspace.ipynb file

# (iii). Preparation

>- Create a module called prepare.py to hold all functions required to prepare the data for exploration including: 
     - Remove duplicates, empty spaces, encode data, drop unnecessary columns and data outliers, rename columns. 
     - Split the data into train, validate and test sets in ratios: 56% : 24% : 20% respectively.


# (iv). Exploration

>- With cleaned data prepared from preparion phase, ensure no data leakage and use train subset.
>- Utelize the initial questions to guide the project explorations.
>- Create visualizations to explain the relationships observed.
>- Perform statistical test to infer key driveres through feature engineering.
>- Document takeaways that guide the project to modeling.

# (v). Modeling
>- Utilize python Sklearn libraries to create, fit and test models in the zillow workspace.ipynb file
>- Predict the target variables 
>- Evaluate the results on the in-sample predictions
>- Select the best model, and use on test subsets for out-of-sample observations.

# (vi). Delivery

>- A final report with summarized results is saved in the zillow_report workbook.
>- Deliverables include a 5 minute presentation through Zoom WebCast with the audience of Zillow Data Science Team. 
>- The key drivers for asssessed tax values stated clearly and best perfoming model presented backed by figures and visul charts. 
>- Deployment of the entire code and workbooks in public Data Scientist GitHub Account with strict exclusion of sensitive database access information through .gitignore.py. 
>- Create this** ReadMe.md file with all steps required to reproduce this test.

# Appendix

Data Dictionary 

|Column | Description | Dtype|
|--------- | --------- | ----------- |
|bed_count | The number of bedrooms | float64 |
|bath_count | The number of bathrooms | float64 |
|square_feet | Square footage of property | float64 |
|tax_value | Property tax value dollar amount | float64 |
|year_built | Year the property was built | int64 |
|fips | Federal Information Processing Standard code | int64 |
|city | City property located | str |
|age | The age of home till 2017 | int64 |
|age_bin | Binned age of home till 2017 | int64 |
|acres | lotsizesquarefeet / 43560 | float64 |
|acres_bin | Binned acres columns (lotsizesquarefeet / 43560) | float64 |
|sqft_bin | Binned calculatedfinishedsquarefeet | float64 |
|bedrooms_bin | Binned bedroomcnt | float64 |
|structure_amount_per_sqft | Feature column (structuretaxvaluedollarcnt/df.calculatedfinishedsquarefeet) | float64 |
|trans_day | The day of month home transactioned | int64 |
|tax_rate | taxamount/ taxvaluedollarcnt * 100 | float64 |


|structure_amount_sqft_bin | Binned columns of structure_amount_per_sqft | float64 |



# To Reconstruct this Project

>- You'll require own env.py file to store query connection credentials(access rights to CodeUp SQL is required).
>- Read this ReadMe.md file fully and make necessary files
>- Set up .gitignore file and ignore env.py, *.csv files
>- Create and Repository directory on GitHub.com
>- Follow instructions above and run the final zillow_workspace report.


# Modeling 
### Perform Linear Regression, Polynomial Regression and Tweedie Regression (GLM).
### Determine best model for prediction of assessed tax value.


# Key Findings 
- > ### Modeling Summary 
- - Baseline Log Error Value: __0.19__
- Linear Regression Log Error Value (best model on test data): __0.1590__

# Future Study on Unseen Data
- With more time, create new unseen features that in combination or slicinf thereof will predict assessed value.
- Heat map shows very strong correlation between bath count and square feet. How are these two features alone affect assessed value?
