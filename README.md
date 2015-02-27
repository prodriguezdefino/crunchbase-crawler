# Crunchbase crawler
A python script to extract Crunchbase organization's information through .

All coma characters are substituted with ```|||``` (triple pipes) in order to scape data in the csv file. 

The variable ```user_key``` should be modified in order to call Crunchbase's API in a correct maner. Also it's posible to configure the starting page for the crawler with the variable ```starting_page``` and the ordering of the results with ```order```, this allows to transverse the dataset in both directions (from newest to oldest and vice versa).

## Initial setup

It's recommended to start running the script using the next configuration:
```
	user_key = <your-user-key>
	starting_page = 0
	order = 'ASC'
```
This will start retrieving the information from the oldest modified item to the newest. Since the dataset in Crunchbase it's pretty big (380000 organizations and counting) it will take a while to retrieve everything from scratch (and more taking into account API soft caps).

## Crunchbase API cap 
With 25000 calls per month (defined cap for the free key request) => 6250 per week (if the process runs weekly) => it takes 2,5 day to consume weekly cap (2,5k calls per day, tops) => so we can use 2100~ calls per process day (if we use 3 days to run the initial load process).

So, currently there are 330~ pages of organization's information (1000 items per page), for each of the items we need to access the details (using a separate API call). Consuming 6250 API calls per week then it would take 53~ weeks to complete the whole dataset. 

Each item comes with a created date and also an updated date, so after initial load up (once we obtained an up to day image of the data in Crunchbase), we should then keep an eye on updated items since our last run event. To achieve that one can change the ```order``` configuration so the script will start with the latest updates in the dataset reducing the amount of API calls to be made to Crunchbase. 

