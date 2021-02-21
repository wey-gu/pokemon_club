# Pokemon Club

This is a DEMO Project for:

- Blog: https://note.siwei.info/pokemon-club-a-demo-app-with-nebula-graph/ 
- video demo: `To be done` 

Today, let's build a new SNS for the Pokemon Trainers, the Pokemon Clubhouse ;)

Pokemon Club is targeting to connect all Pokemon Trainers for their meetup or grouping to fight in certain Pokemon Go Gym.

Like FB or Linkedin, we for sure have the User System with relational DB backed and users metadata of age, avatar, location, and Pokemons she owned, etc. Users as a trainer can create meetups and share posts in Pokemon Club and her friends can get the news feed and comment, join or chat to her.

Apart from the main features, we will only focus on one feature to help trainers explore new friends recommended by the App, based on the Pokemons this trainer owns.

Now we assume either in streaming/ real-time or the batch way, we had put trainer and pokemon relationship in our Nebula Graph DB, and then to create a humble API to get the recommended trainer friends:

```asciiarmor
/v1/recommended_friends/<user>
     +
     |          +--------------+         +----------------+
     |          |              |         |                |
     +---------->  API Server  +--------->  Nebula Graph  |
                |              |         |                |
                +--------------+         +----------------+
```

## Build and Run

You can run it locally:

```bash
pip install -r requirements.txt
export NG_ENDPOINTS="<graphd_host1>:9669,<graphd_host2>:9669,"
gunicorn --bind :$PORT main:app --workers 1 --threads 1 --timeout 60
```

Or via GCP Cloud Run:

```bash
export PROPJECT_ID=<GCP_PROJECT_ID>
# build locally(I know we can/should build in GCP, let's do it locally this time haha) and push to GCP Container Regsitery
docker build -t gcr.io/$PROPJECT_ID/pokemon_club:v1 .
docker push gcr.io/$PROPJECT_ID/pokemon_club:v1

# deploy to Cloud Run
gcloud run deploy pokemon-club-v1 \
    --image gcr.io/$PROPJECT_ID/pokemon_club:v1 \
    --region us-west1 \
    --platform managed \
    --memory 128Mi
# goto Cloud Web Console: https://console.cloud.google.com/run/detail/us-west1/pokemon-club-v1
# Edit and Deploy New Version --> VARIABLES
# add Env VAR: NG_ENDPOINTS with Value: <public_graphd_host1>:9669
# click Deploy
```



## Verify it

```bash
$curl https://pokemon-club-v1-****.a.run.app/v1/recommended_friends/Tom | jq
[
  "Sue",
  "Wey",
  "Jerry"
]
```

