from app import create_app, db
from app.models import Task, User, Post

from flask import render_template
from app.email import send_email

from rq import get_current_job

import sys
import time
import json


def _set_task_progress(progress):
    job = get_current_job()
    if job:
        job.meta['progress'] = progress
        job.save_meta()
        task = Task.query.get(job.get_id())
        task.user.add_notifications('task_progress', {'task_id': job.get_id(), 'progress': progress})

        if progress >= 100:
            task.complete = True

        db.session.commit()


def export_posts(user_id):
    try:
        user = User.query.get(user_id)
        _set_task_progress(0)
        data = []
        total_post_count = user.posts.count()
        for i, post in enumerate(user.posts.order_by(Post.timestamp.asc())):
            data.append(
                {
                    'body': post.body,
                    'timestamp': post.timestamp.isoformat() + 'Z'
                }
            )
            time.sleep(5)
            _set_task_progress(100 * i // total_post_count)

        send_email(
            'YOUR POSTS',
            sender=app.config['ADMINS'][0],
            recipients=user.email,
            text_body=render_template('email/export_posts.txt', user=user),
            html_body=render_template('email/export_posts.html', user=user),
            attachments=[('posts.json', 'application/json', json.dumps({'posts': data}, indent=4))],
            sync=True
        )
    except:
        _set_task_progress(100)
        app.logger.error('Unhandled exception', exc_info=sys.exc_info())


app = create_app()
app.app_context().push()
