import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

app = Flask(__name__)

db = MongoClient(os.environ.get('MONGODB_URI'))[os.environ.get('DB_NAME')]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/bucket', methods=['POST'])
def bucket_post():
    bucket = request.form['bucket_give']
    db.bucket.insert_one({
        'num': db.bucket.count_documents({}) + 1,
        'bucket': bucket,
        'done': 0
    })
    return jsonify({'msg': 'data saved!'})

@app.route('/bucket', methods=['GET'])
def bucket_get():
    bucket_lists = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'buckets': bucket_lists})

@app.route('/bucket/done', methods=['POST'])
def bucket_done():
    db.bucket.update_one({'num': int(request.form['num_give'])}, {'$set': {'done': 1}})
    return jsonify({'msg': 'update done!'})

@app.route('/delete', methods=['POST'])
def bucket_delete():
    db.bucket.delete_one({'num': int(request.form['num_give'])})
    return jsonify({'msg': 'delete done!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5555, debug=True)