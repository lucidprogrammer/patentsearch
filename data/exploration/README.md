# Granted Patents

[PEDS JSON](https://ped.uspto.gov/peds/) does not have information which can be used straight away. It has only the overall metadata like patent number and transactions, dates etc.

[bulk data repo](https://bulkdata.uspto.gov) is more promising. For example, [full text](https://bulkdata.uspto.gov/data/patent/grant/redbook/fulltext/2019/) is updated every Tuesday. I downloaded the latest, however that also did not contain abstract or full text.

I then realised the reason they don't have the data in the said xmls or json, is because the actual text data is in the application downloads.

# Patent Applications
Application data is updated every Thursday.
I initially downloaded the [ Attached is a sample xml which has abstract](https://github.com/lucidprogrammer/patentsearch/files/2868529/last.txt)(it is attached as a text file in this)
The one I downloaded for the date 2019-02-14 00:05 has 7720 xml documents. ie 7720 abstracts.

 [application full text](https://bulkdata.uspto.gov/data/patent/application/redbook/fulltext/2019/).
[sample of ful text application split from the download](https://github.com/lucidprogrammer/patentsearch/files/2869256/0.xml.txt)


# Normalised data
The one which is promising enough is from [patentsview](http://www.patentsview.org/download/). It has normalised data. However it is not clear on the update frequency and when it will get updated next etc. As of now, it is updated till Nov 2018. This is exactly what is needed and it is fully pre-processed and ready for injection directly to a SQL data. As you can see it is fully normalised.

# Approach to take
As of now we can take any of the three approaches as outlined below to solve the data problem, with my understanding of what is available freely.
## Just use the normalised data from patents view
This seems a good approach as the ingestion work is almost nil as the processing is almost done.
Risk Factor: No idea of next update, Currently lagging by 2 months.
## use applications directly
Not sure if the end customers of dmass wants to see only the approved applications.
Risk Factor: Heavy work with applications over many years.
## along with all applications ingest granted patents and drill only granted.
ideal way, but tough road.

I am leaning towards the usage of patents view normalised data. If more info can be enquired from them on any of their sla (it is free - i dont see them talking about update frequency in their site) and any copyright issues.




Refer to [data_exploration](data_exploration.ipynb)
