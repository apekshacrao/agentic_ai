from flask import Flask, jsonify, render_template, request

from movie_generator import MovieGenerator, load_movie_data


app = Flask(__name__)
generator = MovieGenerator(load_movie_data())


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/options")
def options():
    return jsonify(generator.options())


@app.get("/api/movies")
def movies():
    return jsonify({"movies": generator.saved_movies})


@app.post("/api/generate")
def generate():
    details = request.get_json(silent=True) or {}
    try:
        project = generator.generate(details)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(project)


@app.post("/api/movies")
def save_movie():
    project = request.get_json(silent=True) or {}
    try:
        saved = generator.save(project)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(saved), 201


@app.delete("/api/movies/<movie_id>")
def delete_movie(movie_id):
    if not generator.delete(movie_id):
        return jsonify({"error": "Movie project not found."}), 404
    return jsonify({"message": "Movie project deleted."})


if __name__ == "__main__":
    app.run(debug=True)
