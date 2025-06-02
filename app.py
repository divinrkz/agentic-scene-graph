import json
import openai
from flask import Flask, request, jsonify, send_file, render_template, url_for

# Initialize app and folders
app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='static',
    template_folder='templates'
)
# Home page
@app.route('/')
def home():
    return render_template("index.html")

# Layout generation route
@app.route('/generate_layout', methods=['POST'])
def generate_layout():
    data = request.json
    space_type = data["spaceType"]
    width = data["width"]
    height = data["height"]
    length = data["length"]
    custom_catalog = data["furnitureCatalog"]

    catalog_dict = {item["name"]: item["dimensions"] for item in custom_catalog}

    prompt = f"""
    Generate ONLY a JSON layout for a {space_type} with dimensions width: {width}, height: {height}, length: {length} (in feet).
    Use this furniture catalog: {catalog_dict}.
    You do not need to use all items. Ensure furniture fits and pathways are clear.
    Return ONLY JSON, no extra text.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    layout_text = response['choices'][0]['message']['content']
    try:
        layout_json = json.loads(layout_text)
    except json.JSONDecodeError:
        return jsonify({"error": "Invalid JSON returned by model"}), 500

    layout_json["room_size"] = {"width": width, "height": height, "length": length}
    layout_json["space_type"] = space_type

    with open("room_layout.json", "w") as f:
        json.dump(layout_json, f, indent=4)

    return render_template("layout_result.html", layout_json=layout_json)


# Download route
@app.route('/download_layout')
def download_layout():
    return send_file("room_layout.json", as_attachment=True)

# Blender code generation
@app.route('/generate_blender_code')
def generate_blender_code():
    with open("room_layout.json", "r") as f:
        layout_data = f.read()

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"""
            Generate a complete Blender Python script using this JSON layout: {layout_data}.
            Use unit cubes, then scale them to width × depth × height.
            Create the room and furniture as 3D objects at correct sizes and positions.
            Return ONLY code. No comments or extra text.
            """
        }]
    )

    blender_code = response['choices'][0]['message']['content']
    with open("blender_layout.py", "w") as f:
        f.write(blender_code)

    return render_template("blender_result.html", blender_code=blender_code)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
