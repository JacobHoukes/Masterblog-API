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


@app.route("/api/posts", methods=["GET"])
def get_posts():
    return jsonify(POSTS)


@app.route("/api/posts", methods=["POST"])
def add_post():
    """Add a new blog post if valid title and content are provided."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request body"}), 400

    missing_fields = []
    if "title" not in data or not data["title"].strip():
        missing_fields.append("title")
    if "content" not in data or not data["content"].strip():
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


@app.route("/api/posts/<id>", methods=["DELETE"])
def delete_post(id):
    """This function loops through the posts to find the one with the given ID"""
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "Invalid post ID. It must be a number."}), 400
    for post in POSTS:
        if post["id"] == id:
            POSTS.remove(post)
            return jsonify({"message": f"Post with id {id} has been deleted successfully."}), 200
    return jsonify({"error": f"Post with id {id} not found."}), 404


@app.route('/api/posts/<id>', methods=['PUT'])
def update_post(id):
    """This function updates the title and/or content of a blog post by its ID."""
    try:
        id = int(id)
    except ValueError:
        return jsonify({"error": "Invalid post ID. It must be a number."}), 400
    for post in POSTS:
        if post["id"] == id:
            data = request.get_json()
            new_title = data.get("title")
            new_content = data.get("content")
            if new_title:
                post["title"] = new_title
            if new_content:
                post["content"] = new_content
            return jsonify(post), 200
    return jsonify({"error": f"Post with id {id} not found."}), 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
