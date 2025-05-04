from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def generate_new_id():
    """This function generates unique IDs for ech blog post."""
    if not POSTS:
        return 1
    return max(post["id"] for post in POSTS) + 1


@app.route('/api/posts', methods=['GET'])
def get_posts():
    return jsonify(POSTS)


@app.route('/api/posts', methods=['POST'])
def add_post():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request body"}), 400

    missing_fields = []
    if 'title' not in data or not data['title'].strip():
        missing_fields.append("title")
    if 'content' not in data or not data['content'].strip():
        missing_fields.append("content")
    if missing_fields:
        return jsonify({"error": f"Missing or empty fields: {', '.join(missing_fields)}"}), 400

    new_post = {
        "id": generate_new_id(),
        "title": data["title"],
        "content": data["content"]
    }
    POSTS.append(new_post)
    return jsonify(new_post), 201


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
