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
    """This function adds a new blog post if valid title and content are provided."""
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


@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    """This function searches for blog posts by title and/or content based on query parameters."""
    title_query = request.args.get('title')
    content_query = request.args.get('content')
    if title_query:
        title_query = title_query.lower()
    if content_query:
        content_query = content_query.lower()

    matching_posts = []
    for post in POSTS:
        title_matches = title_query in post["title"].lower() if title_query else False
        content_matches = content_query in post["content"].lower() if content_query else False
        if title_matches or content_matches:
            matching_posts.append(post)
    return jsonify(matching_posts), 200


@app.route('/api/posts', methods=['GET'])
def list_posts():
    """This function returns all blog posts, with optional sorting by title or content."""
    sort = request.args.get('sort')
    direction = request.args.get('direction')
    sorted_posts = POSTS.copy()
    if sort:
        if sort not in ['title', 'content']:
            return jsonify({"error": "Invalid sort field. Use 'title' or 'content'."}), 400
        if direction and direction not in ['asc', 'desc']:
            return jsonify({"error": "Invalid direction. Use 'asc' or 'desc'."}), 400
        reverse = (direction == 'desc')
        sorted_posts.sort(key=lambda post: post.get(sort, '').lower(), reverse=reverse)
    return jsonify(sorted_posts), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
