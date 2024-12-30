import os
import praw
from flask import Flask, request, render_template

app = Flask(__name__)

# ==================
# 1. REDDIT AUTH SETUP
# ==================
# Replace these with your real credentials
REDDIT_CLIENT_ID = "601N0-NA9UzVghd794XUSw"
REDDIT_CLIENT_SECRET = "ZoadxSywbzcKD--cvthcdAJQPtE6fQ"
REDDIT_USER_AGENT = "Opinionator/1.0 by No_Vegetable6570"

# We initialize the PRAW Reddit instance.
# For a "script" type app, you might also use username and password, but
# for demonstration, we'll just do read-only with client_id + client_secret + user_agent:
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
    # If you do need username/password:
    # username="YOUR_REDDIT_USERNAME",
    # password="YOUR_REDDIT_PASSWORD",
)

# ==================
# 2. HOME ROUTE - Show the Form
# ==================
@app.route('/')
def index():
    """
    Renders the main page with the input form and the text area.
    """
    return render_template('index.html', scraped_data='')

# ==================
# 3. SCRAPE ROUTE - Process Form Submission
# ==================
@app.route('/scrape', methods=['POST'])
def scrape():
    """
    When the user hits the "Scrape" button, 
    we'll grab the Reddit URL, scrape comments, 
    and display them in the text area.
    """
    thread_url = request.form.get('reddit_url', '')

    # Validate that we actually received a URL
    if not thread_url:
        # Return with an error in the text area if no URL was provided
        return render_template('index.html', 
                               scraped_data="Error: No URL was provided.")

    try:
        scraped_text = scrape_comments(thread_url)
    except Exception as e:
        # Basic error handling
        error_message = f"An error occurred while scraping: {str(e)}"
        return render_template('index.html', scraped_data=error_message)

    return render_template('index.html', scraped_data=scraped_text)

# ==================
# 4. HELPER FUNCTION
# ==================
def scrape_comments(thread_url):
    """
    Given a Reddit submission URL, fetch all comments (including hidden/nested),
    and return a big text string containing each comment's text, upvote count,
    and downvote count.
    """

    # 1. Get the submission object
    submission = reddit.submission(url=thread_url)

    # 2. Replace More Comments (so we load everything, not just top-level)
    submission.comments.replace_more(limit=None)

    # 3. Flatten the comment tree into a list (includes nested replies)
    all_comments = submission.comments.list()

    # 4. Iterate and build the final string
    output_lines = []
    for comment in all_comments:
        # "comment.body" is the raw comment text
        comment_text = comment.body
        # "comment.ups" is how many upvotes
        ups = comment.ups
        # "comment.downs" is how many downvotes (may sometimes be 0 or hidden; depends on Reddit)
        downs = comment.downs

        # Format however you like. For example:
        line = f"{comment_text}\nUpvotes: {ups}  Downvotes: {downs}\n{'-'*80}"
        output_lines.append(line)

    # Join all comments with a couple of newlines
    final_output = "\n\n".join(output_lines)
    return final_output

# ==================
# 5. RUN THE FLASK APP (Localhost)
# ==================
if __name__ == '__main__':
    # You can customize the port if you like
    app.run(debug=True, port=5000)
