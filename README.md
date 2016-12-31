# TwitterNetwork
Finds the Twitter accounts that are followed the most by your friends (the people you follow)
## Usage
1. Use [this](https://themepacific.com/how-to-generate-api-key-consumer-token-access-key-for-twitter-oauth/994/) link to generate the needed secret keys.
2. Put the keys you obtained in a file called secrets.py file, along with your username, specifically:  
 * consumer_secret 
  * consumer_key
 * access_token 
 * access_token_secret
 * username 

3. Run main.py, beware that it's pretty slow (it takes an hour for every 60 people you follow) because of Twitter's API rate limitations.
4. Results will be in the accounts.json file.
5. If you want them in a pretty HTML table, copy the sorterdAccounts.json file to the HTML floder, open the table.html file in a webserver and they should be there
6. ..Profit?

## Contribution
There are many optimizations to be made in the code, especially to lookup for usernames (should be done in bulk instead of a call per user) but I don't have the time for it. There's a big room for improvement, and you're welcome if you'd like to help.
