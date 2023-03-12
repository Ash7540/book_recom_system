from flask import Flask,render_template,request
import pickle
import numpy as np

popular_data = pickle.load(open('popular.pkl', 'rb'))
p_table = pickle.load(open('p_table.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
scores = pickle.load(open('scores.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name=list(popular_data['Book-Title'].values),
                           author=list(popular_data['Book-Author'].values),
                           image=list(popular_data['Image-URL-M'].values),
                           votes=list(popular_data['num_ratings'].values),
                           rating=list(popular_data['avg_rating'].values)
                           )


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')


@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    index = np.where(p_table.index == user_input)[0][0]
    similar_items = sorted(
        list(enumerate(scores[index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == p_table.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates(
            'Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)

    return render_template('recommend.html', data=data)

if __name__=='__main__':
    app.run(debug=True)