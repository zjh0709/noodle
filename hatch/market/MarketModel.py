import pymongo
import os
import pickle


class MarketModel(object):

    data = []

    def read_data(self):
        pkl_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "market_data.pkl")
        if os.path.isfile(pkl_file):
            self.data = pickle.load(open(pkl_file, "rb"))
        else:
            db = pymongo.MongoClient("master", port=17585).get_database("noodle")
            cursor = db.get_collection("market")\
                .find({}, {"_id": 0, "ts_code": 0})
            self.data = list(cursor)
            pickle.dump(self.data, open(pkl_file, "wb"))
        return self.data


if __name__ == '__main__':
    m = MarketModel()
    d = m.read_data()
    print(d[0])
