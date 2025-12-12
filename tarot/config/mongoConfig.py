import mongoengine

# Connect to the MongoDB database
mongoengine.connect(
    db='tarotdb',
    host='localhost',
    port=27017,
)