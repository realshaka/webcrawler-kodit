First, I recognized all information I need is in Meta with name = "kodit:apartment" in every apartment link. Then I decided get the links of all apartments  from "https://kodit.io/fi/buy/" and went through them to collect data of all aparments. 
After that, I wanted to add more information about apartments' prices. I downloaded csv file of house pricing in Finland 2018 from Statistic Finland(stat.fi). Then I compared Kodit apartments' price with the stat base on location and number of rooms in the apartments. Because I knew from my friends that they usually negotiate 5% of price so I added that figure to the comparison.  
Finally I saved all result to result.json and posted to the given link. I tested my python script with a local json server and it ran well. 
If you don't use BeautifulSoup please install it before running. 
You can test with the local json server. First install with "npm install -g json-server" then run "json-server db.json".
