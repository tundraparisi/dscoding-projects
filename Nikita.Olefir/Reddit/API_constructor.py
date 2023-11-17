from Reddit_API_Wrapper import reddit
import pandas as pd

def comments_extractor(subreddit_name:str,submission_id:str):
    subreddit_name = subreddit_name 
    submission_id = submission_id
    submission = reddit.submission(id=submission_id)
    all_comments = []
    submission.comments.replace_more(limit=None)  
    for comment in submission.comments.list():
        all_comments.append({
        'author': comment.author.name if comment.author else '[deleted]',
        'body': comment.body,
        'score': comment.score,
        'created_utc': comment.created_utc
        })
    comments_df = pd.DataFrame(all_comments)
    print(comments_df)
    