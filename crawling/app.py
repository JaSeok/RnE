from flask import Flask, request
import os
import recognition1
import recognition2
import refine1
import refine2

app = Flask(__name__)


def initialize_file(file_path):
    """
    Initialize the file by clearing its content.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        file.write("")  # Clear the file content


def run_pipeline(url):
    

    # Initialize webpage_text.txt
    content_file = "webpage_text.txt"
    initialize_file(content_file)

    # Run recognition1

    recognition1.main(url)

    # Check if webpage_text.txt is empty
    if not os.path.exists(content_file):
        recognition2.main(url)
    else:
        with open(content_file, "r", encoding="utf-8") as file:
            content = file.read().strip()
            
            if not content:
                recognition2.main(url)

    # Run refine1 and refine2

    refine1.main()

    refine2.main()


@app.route("/", methods=["GET"])
def index():
    """
    Main Flask route for processing URL passed as a query parameter.
    """
    title = None
    content = None
    message = None

    url = request.args.get("url")
    if url:
        # File paths
        title_file = "webpage_title.txt"
        content_file = "webpage_text.txt"

        # Run the pipeline
        run_pipeline(url)

        # Read the title and content from files
        if os.path.exists(title_file):
            with open(title_file, "r", encoding="utf-8") as file:
                title = file.read().strip()
        if os.path.exists(content_file):
            with open(content_file, "r", encoding="utf-8") as file:
                content = file.read().strip()

        # Return success message and file content
        message = "HTTP 200 OK"
    else:
        message = "URL Error"

    return {"title": title, "content": content}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1225)
