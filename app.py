from flask import Flask, render_template, request
from repo_find import get

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/list", methods=["GET"])
def get_my_list():
    org = request.args.get("org")
    n = request.args.get("N")
    m = request.args.get("M")
    page_no = request.args.get("page_no", "1")

    repos, next_page_link, previous_page_link = get(org, int(n), int(m), page_no)
    org_name = str(org)

    if repos == "404":
        return "There is an error with organization or one of the values of n or m is not positive"
    return render_template(
        "repo_list.html",
        repos=repos,
        org=org_name.upper(),
        next_page_link=next_page_link,
        previous_page_link=previous_page_link,
    )


if __name__ == "__main__":
    app.run(debug=True)
