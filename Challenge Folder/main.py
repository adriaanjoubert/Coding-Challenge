"""This module is called by Google App Engine

It looks for "app" in the "main.py" class to run flask with gunicorn"""

import time
import logging

import pandas as pd
import psycopg2 as pg

from flask import Flask, render_template, request
from flask.logging import create_logger

from test_database import DBClient

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)
log = create_logger(app)
log.info('------ DEBUG LOGGING STARTS HERE -------')

db_client = DBClient()


@app.route('/', methods=['GET'])
def index():
    """Runs when GET requested on '/'.

    Returns:
        render_template (flask): index.html
    """
    log.info("@ index()")

    return render_template('at-index.html')


@app.route('/test/<int:item_count>', methods=['GET'])
def at_test(item_count=None):
    """Runs when GET requested on '/login/<user_id>'.

    The main endpoint to test the time it takes to process the items in the database.

    Args:
        item_count=None (str): sets the number of items to count after the '/test/' path

    Return:
        render_template (flask): html template based on logic from this app"""
    log.info("@ at_test(item_count=None): %s", item_count)

    #  ˅This is the script that measures the performance, not allowed to edit this section.˅ 
    hit_time = time.time()
    #  ˄This is the script that measures the performance, not allowed to edit this section.˄

    if item_count > 100:
        return render_template(
            'at-error.html',
            message="More then 100 items selected, too many. Item Count: ",
            error=item_count
        )

    person_query = request.args.get('person', type=str)
    type_query = request.args.get('type', type=str)

    if not type_query:
        if person_query:
            return render_template(
                'at-error.html',
                message="Please select either Text or JSON",
                error='',
            )
        return render_template(
            'at-json.html',
            records=pd.DataFrame(),
            data='{}',
            item_count=item_count,
            hit=hit_time,
        )

    # <- get user info
    try:
        data_json = db_client.get_json(item_count=item_count, person=person_query)
    except pg.Error as error:
        return render_template('at-error.html', message="There was an error.", error=error)

    if type_query == "text":
        return render_template(
            'at-text.html',
            data=data_json,
            item_count=item_count,
            hit=hit_time
        )

    return render_template(
        'at-json.html',
        data=data_json,
        item_count=item_count,
        hit=hit_time
    )


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google app
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # app Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=5000, debug=True)
