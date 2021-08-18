import collections
from itertools import chain
import numpy as np
import tensorflow._api.v2.compat.v1 as tf
tf.disable_v2_behavior()
import pandas as pd
from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo

# from libs.recommendation import get_from_db
# from libs.recommendation import insert_in_db

# get from db
#사용자에게 해당하는 태그 불러오기
def get_keywords():
    app = Flask(__name__)
    app.debug = True

    # response order
    app.config["JSON_SORT_KEYS"] = False
    # DB = dbConnection.DB
    app.config["MONGO_URI"] = "mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin"
    mongo = PyMongo(app)

    cursor = mongo.db.user.find({},
                                {
                                    "_id": 0,
                                    "name": 0,
                                    "nickname": 0,
                                    "intro": 0,
                                    "profileImage": 0,
                                    "scraps": 0,
                                    "likes": 0,
                                    "followers": 0,
                                    "followings": 0
                                }
                                )
    list_cur = list(cursor)
    # print(list_cur)
    result_list = ""
    for x in list_cur:
        result_string = ""
        result_string += x['email']
        result_string += " "
        # print(x) #{'email': 'parktae27@admin.com', 'tags': ['물집', '완주', '지구', '사람', '마라톤', '무릎', '슈퍼맨', '포기', '운동']
        for tag in x['tags']:
            result_string += tag
            result_string += " "
            # print(result_string)
        result_list += result_string
        result_list += "\n"

    '''
    sciencelife@admin.com 사랑 과학 행복 사랑 연애 키스 과학 인문학 교양
    wivlabs@admin.com 광고 페이스북 IT 타겟 효율 키스 광고성과 인문학 구글

    result_list 이러한 형태
    '''
    return result_list





vocabulary_size = 400000


def build_dataset(sentences):
    words = ''.join(sentences).split()
    count = [['UNK', -1]]
    count.extend(collections.Counter(words).most_common(vocabulary_size - 1))
    dictionary = dict()
    for word, _ in count:
        dictionary[word] = len(dictionary)

    unk_count = 0
    sent_data = []
    for sentence in sentences:
        data = []
        for word in sentence.split():
            if word in dictionary:
                index = dictionary[word]
            else:
                index = 0  # dictionary['UNK']
                unk_count = unk_count + 1
            data.append(index)
        sent_data.append(data)
    count[0][1] = unk_count
    reverse_dictionary = dict(zip(dictionary.values(), dictionary.keys()))
    return sent_data, count, dictionary, reverse_dictionary


############################
# Chunk the data to be passed into the tensorflow Model
###########################
data_idx = 0


def generate_batch(batch_size):
    global data_idx

    if data_idx + batch_size < instances:
        batch_labels = labels[data_idx:data_idx + batch_size]
        batch_doc_data = doc[data_idx:data_idx + batch_size]
        batch_word_data = context[data_idx:data_idx + batch_size]
        data_idx += batch_size
    else:
        overlay = batch_size - (instances - data_idx)
        batch_labels = np.vstack([labels[data_idx:instances], labels[:overlay]])
        batch_doc_data = np.vstack([doc[data_idx:instances], doc[:overlay]])
        batch_word_data = np.vstack([context[data_idx:instances], context[:overlay]])
        data_idx = overlay
    batch_word_data = np.reshape(batch_word_data, (-1, 1))

    return batch_labels, batch_word_data, batch_doc_data


def most_similar(user_id, size):
    if user_id in sentences_df_indexed.index:
        user_index = sentences_df_indexed.loc[user_id]['index']
        dist = final_doc_embeddings.dot(final_doc_embeddings[user_index][:, None])
        closest_doc = np.argsort(dist, axis=0)[-size:][::-1]
        furthest_doc = np.argsort(dist, axis=0)[0][::-1]

        result = []
        for idx, item in enumerate(closest_doc):
            user = sentences[closest_doc[idx][0]].split()[0]
            dist_value = dist[item][0][0]
            result.append([user, dist_value])
        return result


#insert into db
def insert_into():
    from flask_pymongo import PyMongo, MongoClient
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin"
    mongo = PyMongo(app)

    # DB에 사용자 주입
    client = MongoClient('mongodb://onego:test123@onegodev.ddns.net:2727/onego?authsource=admin')
    db = client['onego']
    collection = db['recommend']

    cursor = mongo.db.user.find({},
                                {
                                    "_id": 0,
                                    "name": 0,
                                    "nickname": 0,
                                    "intro": 0,
                                    "profileImage": 0,
                                    "scraps": 0,
                                    "likes": 0,
                                    "followers": 0,
                                    "followings": 0,
                                    "tags": 0,
                                    "nickName": 0
                                }
                                )
    want_users = list(cursor)
    list_want_user = []
    for x in want_users:
        list_want_user.append(x['email'])

    for want_user in list_want_user:
        most = most_similar(want_user, 11)
        list_sim = []
        for sim in most[1:11]:
            list_sim.append(sim[0])

            recommend = {
                "email": want_user,
                "recommendation": list_sim
            }
        print(recommend)
        recommended = db.recommend
        recommended.insert(recommend)
    return 'insert_finish'


if __name__ == '__main__':

    words = []
    file = get_keywords()
    for f in file:
        words.append(f)
    words = list(chain.from_iterable(words))
    words = ''.join(words)[:-1]
    sentences = words.split('\n')
    sentences_df = pd.DataFrame(sentences)

    sentences_df['user'] = sentences_df[0].apply(lambda x: x.split()[0])
    sentences_df['words'] = sentences_df[0].apply(lambda x: ' '.join(x.split()[1:]))
    sentences_df['words_list'] = sentences_df[0].apply(lambda x: x.split())
    sentences_df['words_num'] = sentences_df[0].apply(lambda x: len(x.split()))
    sentences_df_indexed = sentences_df.reset_index().set_index('user')

    data, count, dictionary, reverse_dictionary = build_dataset(sentences_df_indexed['words'].tolist())
    print('Most common words (+UNK)', count[:5])
    print('Sample data', data[:2])
    # del words  # Hint to reduce memory.

    skip_window = 5  # 주변 단어의 범위 한정
    instances = 0

    # Pad sentence with skip_windows
    for i in range(len(data)):
        data[i] = [vocabulary_size] * skip_window + data[i] + [vocabulary_size] * skip_window

    # Check how many training samples that we get
    for sentence in data:
        instances += len(sentence) - 2 * skip_window
    print(instances)  # 22886

    context = np.zeros((instances, skip_window * 2 + 1), dtype=np.int32)
    labels = np.zeros((instances, 1), dtype=np.int32)
    doc = np.zeros((instances, 1), dtype=np.int32)

    k = 0
    for doc_id, sentence in enumerate(data):
        for i in range(skip_window, len(sentence) - skip_window):
            context[k] = sentence[i - skip_window:i + skip_window + 1]  # Get surrounding words
            labels[k] = sentence[i]  # Get target variable
            doc[k] = doc_id
            k += 1

    context = np.delete(context, skip_window, 1)
    # delete the middle word
    # array: context, object: skip_window, axis: 1(가로방향으로 처리)
    # context에서 가로방향으로 skip_window(5)번 인덱스 열 하나 삭제
    print(context)

    shuffle_idx = np.random.permutation(k)  # 랜덤으로 섞은 배열 반환.. (22886,)
    labels = labels[shuffle_idx]  # (22886,1)
    doc = doc[shuffle_idx]  # (22886,1)
    context = context[shuffle_idx]  # (22886,10)

    ## MODEL SAVE

    batch_size = 256  # 0~255
    context_window = 2 * skip_window  # 10
    embedding_size = 50  # Dimension of the embedding vector.
    softmax_width = embedding_size  # +embedding_size2+embedding_size3
    num_sampled = 5  # Number of negative examples to sample.
    sum_ids = np.repeat(np.arange(batch_size), context_window)  # [  0   0   0 ... 255 255 255]
    # np.arange(batch_size)라는 스칼라를 context_window(10)만큼 반복..
    # 즉 sum_ids는 0을 10번, 1을 10번, 2를 10번.... 255를 10번 반복한 array

    len_docs = len(data)

    train_word_dataset = tf.placeholder(tf.int32, shape=[batch_size * context_window])
    train_doc_dataset = tf.placeholder(tf.int32, shape=[batch_size])
    train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])  # placeholder 로 특정 작업을 feed로 지정

    segment_ids = tf.constant(sum_ids, dtype=tf.int32)

    # random_uniform :: (shape, minval, maxval)
    word_embeddings = tf.Variable(tf.random_uniform([vocabulary_size, embedding_size], -1.0, 1.0))
    word_embeddings = tf.concat([word_embeddings, tf.zeros((1, embedding_size))], 0)  # axis =0 가장 바깥 차원 기준으로 붙인다.
    doc_embeddings = tf.Variable(tf.random_uniform([len_docs, embedding_size], -1.0, 1.0))

    softmax_weights = tf.Variable(tf.truncated_normal([vocabulary_size, softmax_width],
                                                      stddev=1.0 / np.sqrt(embedding_size)))
    softmax_biases = tf.Variable(tf.zeros([vocabulary_size]))

    # Model.
    # Look up embeddings for inputs.
    embed_words = tf.segment_mean(tf.nn.embedding_lookup(word_embeddings, train_word_dataset), segment_ids)
    embed_docs = tf.nn.embedding_lookup(doc_embeddings, train_doc_dataset)
    embed = (embed_words + embed_docs) / 2.0  # +embed_hash+embed_users

    # Compute the softmax loss, using a sample of the negative labels each time.
    loss = tf.reduce_mean(tf.nn.nce_loss(softmax_weights, softmax_biases, train_labels,
                                         embed, num_sampled, vocabulary_size))

    # Optimizer.
    optimizer = tf.train.AdagradOptimizer(0.5).minimize(loss)

    norm = tf.sqrt(tf.reduce_sum(tf.square(doc_embeddings), 1, keep_dims=True))
    normalized_doc_embeddings = doc_embeddings / norm

    saver = tf.compat.v1.train.Saver()
    sess = tf.Session()
    sess.run(tf.global_variables_initializer())
    saver.save(sess, './model/user_recommend_model')

    ## READ MODEL

    # 네트워크 생성
    saver = tf.train.import_meta_graph('./model/user_recommend_model.meta')
    # tf.reset_default_graph() # default graph로 초기화

    # 파라미터 로딩
    with tf.Session() as sess:
        new_saver = tf.train.import_meta_graph('./model/user_recommend_model.meta')
        new_saver.restore(sess, tf.train.latest_checkpoint('./model'))

    with tf.Session() as sess:
        saver = tf.train.import_meta_graph('./model/user_recommend_model.meta')
        saver.restore(sess, tf.train.latest_checkpoint('./model'))
        print(sess.run([softmax_weights]))
        print(sess.run([softmax_biases]))

    ## USE MODEL WITH NEW feed_dict
    num_steps = 200001
    step_delta = int(num_steps / 20)

    sess = tf.Session()
    saver = tf.train.import_meta_graph('./model/user_recommend_model.meta')
    saver.restore(sess, tf.train.latest_checkpoint('./model'))

    # create new feed_dict
    graph = tf.get_default_graph()  # 그래프 초기화
    average_loss = 0
    for step in range(num_steps):
        batch_labels, batch_word_data, batch_doc_data = generate_batch(batch_size)
        feed_dict = {train_word_dataset: np.squeeze(batch_word_data),  # np.squeeze로 1차원 배열로 차원 축소
                     train_doc_dataset: np.squeeze(batch_doc_data),
                     train_labels: batch_labels}
        _, l = sess.run([optimizer, loss], feed_dict=feed_dict)

        average_loss += l

        if step % step_delta == 0:
            if step > 0:
                average_loss = average_loss / step_delta
            # The average loss is an estimate of the loss over the last 2000 batches.
            print('Average loss at step %d: %f' % (step, average_loss))

            average_loss = 0

    final_word_embeddings = word_embeddings.eval(session=sess)
    final_word_embeddings_out = softmax_weights.eval(session=sess)
    final_doc_embeddings = normalized_doc_embeddings.eval(session=sess)

    insert_into() # db에 추천 user 식별자 넣음


