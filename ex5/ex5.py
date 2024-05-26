"""written and submitted by David Koplev 208870279 and Rotem Kashani 209073352"""
from pymongo.mongo_client import MongoClient
import textwrap

client = MongoClient("mongodb+srv://rotemkash:rotemkash@cluster0.r18fvtg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
airbnb = client.sample_airbnb
mflix = client.sample_mflix
supplies = client.sample_supplies

def print_results(question_num, query, results):
    output = textwrap.dedent(f"""\
==========================================================
Question: {question_num}

Query:
{query}

Results:
        """)

    results_list = list(results)

    if results_list:
        for row in results_list[:10]:
            output += f"{row}\n\n"
    else:
        output += "No results\n"

    print(output)


query_1a = """
airbnb.listingsAndReviews.aggregate([
    {'$match': {
        'property_type': 'House',
        'number_of_reviews': {'$gt': 50},
        '$or': [
            {'beds': {'$gte': 5}},
            {'beds': {'$lte': 2}}
        ]
    }},
    {'$project': {
        '_id': 1,
        'beds': 1,
        'number_of_reviews': 1,
        'property_type': 1
    }}
])
"""
results_1a = airbnb.listingsAndReviews.aggregate([
    {'$match': {
        'property_type': 'House',
        'number_of_reviews': {'$gt': 50},
        '$or': [
            {'beds': {'$gte': 5}},
            {'beds': {'$lte': 2}}
        ]
    }},
    {'$project': {
        '_id': 1,
        'beds': 1,
        'number_of_reviews': 1,
        'property_type': 1
    }}
])
print_results("1a", query_1a, results_1a)

query_1b = """
airbnb.listingsAndReviews.aggregate([
    { '$match': { 'room_type': 'Private room' } },
    { '$addFields': { 'price_per_person': { '$divide': [ '$price', '$accommodates' ] } } },
    { '$group': {
        '_id': '$address.market',
        'avg_price_per_person': { '$avg': '$price_per_person' },
        'count': { '$sum': 1 }
    }},
    { '$match': { '_id': { '$nin': [null, ''] } } },
    { '$sort': { 'avg_price_per_person': -1 } },
    { '$limit': 5 }
])
"""

results_1b = airbnb.listingsAndReviews.aggregate([
    {'$match': {'room_type': 'Private room'}},
    {'$addFields': {'price_per_person': {'$divide': ['$price', '$accommodates']}}},
    {'$group': {
        '_id': '$address.market',
        'avg_price_per_person': {'$avg': '$price_per_person'},
        'count': {'$sum': 1}
    }},
    {'$match': {'_id': {'$nin': [None, '']}}},
    {'$sort': {'avg_price_per_person': -1}},
    {'$limit': 5}
])

print_results("1b", query_1b, results_1b)

query_1c = """
airbnb.listingsAndReviews.aggregate([
    { '$unwind': '$reviews' },
    { '$group': {
        '_id': '$reviews.reviewer_id',
        'count': { '$sum': 1 }
    }},
    { '$sort': { 'count': -1 } },
    { '$limit': 5 },
    { '$sort': { 'count': 1 } }  
])
"""

results_1c = airbnb.listingsAndReviews.aggregate([
    {'$unwind': '$reviews'},
    {'$group': {
        '_id': '$reviews.reviewer_id',
        'count': {'$sum': 1}
    }},
    {'$sort': {'count': -1}},
    {'$limit': 5},
    {'$sort': {'count': 1}}
])

print_results("1c", query_1c, results_1c)

query_2a = """
mflix.comments.aggregate([
    {
        '$group': {
            '_id': '$movie_id',
            'num_comments': {'$sum': 1}
        }
    },
    {
        '$sort': {'num_comments': -1}
    },
    {
        '$limit': 5
    },
    {
        '$lookup': {
            'from': 'movies',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'movieInfo'
        }
    },
    {
        '$unwind': '$movieInfo'
    },
    {
        '$project': {
            '_id': 1,
            'title': '$movieInfo.title',
            'year': '$movieInfo.year',
            'num_comments': 1
        }
    }
])
"""

results_2a = mflix.comments.aggregate([
    {
        '$group': {
            '_id': '$movie_id',
            'num_comments': {'$sum': 1}
        }
    },
    {
        '$sort': {'num_comments': -1}
    },
    {
        '$limit': 5
    },
    {
        '$lookup': {
            'from': 'movies',
            'localField': '_id',
            'foreignField': '_id',
            'as': 'movieInfo'
        }
    },
    {
        '$unwind': '$movieInfo'
    },
    {
        '$project': {
            '_id': 1,
            'title': '$movieInfo.title',
            'year': '$movieInfo.year',
            'num_comments': 1
        }
    }
])

print_results("2a", query_2a, results_2a)

query_2b = """
db.movies.aggregate([
    {'$match': {'imdb.votes': {'$exists': True, '$ne': 0}}},
    {'$unwind': '$directors'},
    {'$group': {
        '_id': '$directors', 
        'avg_rating': {'$avg': '$imdb.rating'},
        'movies_count': {'$sum': 1}
    }},
    {'$match': {
        'avg_rating': {'$gt': 7},
        'movies_count': {'$gte': 5}
    }},
    {'$sort': {'avg_rating': -1}}
])
"""

results_2b = mflix.movies.aggregate([
    {'$match': {'imdb.votes': {'$exists': True, '$ne': 0}}},
    {'$unwind': '$directors'},
    {'$group': {
        '_id': '$directors',
        'avg_rating': {'$avg': '$imdb.rating'},
        'movies_count': {'$sum': 1}
    }},
    {'$match': {
        'avg_rating': {'$gt': 7},
        'movies_count': {'$gte': 5}
    }},
    {'$sort': {'avg_rating': -1}}
])

print_results("2b", query_2b, results_2b)

query_3a = """
supplies.sales.aggregate([
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.name",
        "average_price": {"$avg": "$items.price"}
    }},
    {"$sort": {"average_price": -1}}
])
"""

results_3a = supplies.sales.aggregate([
    {"$unwind": "$items"},
    {"$group": {
        "_id": "$items.name",
        "average_price": {"$avg": "$items.price"}
    }},
    {"$sort": {"average_price": -1}}
])

print_results("3a", query_3a, results_3a)

query_3b = """
supplies.sales.aggregate([
    {"$unwind": "$items"},
    {"$unwind": "$items.tags"},
    {"$group": {
        "_id": "$items.tags",
        "total_quantity_sold": {"$sum": "$items.quantity"}
    }},
    {"$sort": {"total_quantity_sold": -1}}
])
"""

results_3b = supplies.sales.aggregate([
    {"$unwind": "$items"},
    {"$unwind": "$items.tags"},
    {"$group": {
        "_id": "$items.tags",
        "total_quantity_sold": {"$sum": "$items.quantity"}
    }},
    {"$sort": {"total_quantity_sold": -1}}
])

print_results("3b", query_3b, results_3b)
