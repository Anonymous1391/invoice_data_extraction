import pymongo
import project_config

def get_db():
    url = f"mongodb://localhost:{project_config.MONGODB_PORT_NUMBER}/"
    mongo_client = pymongo.MongoClient(url)

    # create DB
    db = mongo_client[project_config.PROJECT_DB_NAME]
    #create collections
    user_collection = db[project_config.USER_COLLECTION_NAME]
    return user_collection