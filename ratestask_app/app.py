#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import psycopg2
from datetime import datetime
from datetime import timedelta
from contextlib import closing
from psycopg2.extras import execute_values
from bottle import hook, route, request, response, HTTPResponse, run


DB_HOST = os.environ.get('DB_HOST', '127.0.0.1')
DB_PORT = os.environ.get('DB_PORT', 5432)
DB_USER = os.environ.get('DB_USER', 'postgres')
DB_PASS = os.environ.get('DB_PASS')
DB_NAME = os.environ.get('DB_NAME')

pretty_json = dict(indent=2, sort_keys=True, default=str)


@hook('before_request')
def application_json():
    """ All returned data is expected to be in JSON format.
    """
    response.content_type = 'application/json'


class DBSession:
    """ Postgres DB connector.
    """
    def __init__(self, host=DB_HOST, port=DB_PORT, usr=DB_USER, pwd=DB_PASS, db=DB_NAME):
        """ During the initialization attempt to connect to the DB.
        """
        self.connection = psycopg2.connect(host=host, port=port, user=usr, password=pwd, dbname=db)
        self.cursor = self.connection.cursor()

    def __call__(self, *a, **kw):
        """ Calling an object proxies to the execute().
        """
        self.cursor.execute(*a, **kw)
        return self.cursor

    def execute_values(self, *a, **kw):
        """ For speedy multi INSERT.
        """
        execute_values(self.cursor, *a, **kw)
        return self.cursor

    def close(self):
        """ When DB session is over, connections to the server should be ended manually.
        """
        self.cursor.close()
        self.connection.close()


def Error(msg=None, code=400, **kw):
    """ Helper fn. to display errors.
    """
    body = {'error': 'Unknown Error'}
    if msg is not None:
        body['error'] = msg
    if kw:
        body.update(kw)
    return HTTPResponse(json.dumps(body, **pretty_json), code)


def to_dict(cursor):
    """ Add column names to the fetched values.
    """
    rows = cursor.fetchall()
    cols = [desc[0] for desc in cursor.description]
    try:
        return list(dict(zip(cols, row)) for row in rows)
    except Exception:
        return []


def parse_dates(params, keys=['date_from', 'date_to']):
    """ Convert date string to the python datetime.
        When date_to is not declared, make sure its value is None.
    """
    for key in keys:
        if key == 'date_to' and not params.get(key):
            params[key] = None
            continue
        params[key] = datetime.strptime(params[key], '%Y-%m-%d')
    # date_to should not be older or equal to the date_from
    if isinstance(params['date_to'], datetime) and params['date_to'] <= params['date_from']:
        raise RuntimeError()
    return params


def parse_orig_dest_get(params, keys = ['origin', 'destination']):
    """ Normalize origin and destination keys in the GET request.
    """
    for key in keys:
        if len(params[key]) == 5:
            # Port code == 5-character uppercase string
            params[key] = str(params[key]).upper()
        else:
            # Port slug == more than 5-character lowercase string
            params[key] = str(params[key]).lower()
    return params


def parse_orig_dest_post(params, keys = ['origin_code', 'destination_code']):
    """ Normalize origin and destination keys in the POST request.
    """
    for key in keys:
        # Port code must be 5-character uppercase string
        if len(params[key]) != 5:
            raise RuntimeError()
        else:
            params[key] = str(params[key]).upper()
    return params


def parse_price(params):
    """ Normalize price.
    """
    params['price'] = int(params['price'])
    return params


def get_query(params):
    """ Choose correct query based on the origin and destination string length.
    """
    ## Here I'm using Psycopg capability automatically convert Python objects to the SQL literals
    ## (note %(origin)s and %(destination)s variables). Without this the code would be susceptible
    ## to the SQL injection attack, meaning that the attacker could craft a malformed input string
    ## and either access unauthorized data or perform destructive operations on the database.
    base_query = ('SELECT day, ROUND(AVG(price)) average_price '
                  'FROM prices '
                  'INNER JOIN ports orig ON orig_code = orig.code '
                  'INNER JOIN ports dest ON dest_code = dest.code '
                  'WHERE {origin} = %(origin)s AND {destination} = %(destination)s '
                  'AND day BETWEEN %(date_from)s AND %(date_to)s '
                  'GROUP BY day ')
    base_fields = dict(origin='orig_code', destination='dest_code')
    if len(params['origin']) > 5:
        base_fields['origin'] = 'orig.parent_slug'
    if len(params['destination']) > 5:
        base_fields['destination'] = 'dest.parent_slug'
    return base_query.format(**base_fields)


def post_param_list(params, keys = ['origin_code', 'destination_code', 'date_from', 'price']):
    """ When date_to is declared in the params we need to create a list of params
        within the specified date range.
    """
    one_day = timedelta(days=1)
    params_list = [{k: params[k] for k in keys}]
    date_to, date_from = params['date_to'], params['date_from']
    if 'date_to' in params and isinstance(params['date_to'], datetime):
        for x in range((date_to - date_from).days):
            params['date_from'] += one_day
            params_list.append({k: params[k] for k in keys})
    return params_list


# --- ~ ---


@route(['/get'], method=['GET'])
def rates_get():
    """
    Implement an API endpoint that takes the following parameters:
    *date_from, date_to, origin, destination* and returns a list with the
    average prices for each day on a route between *origin* and
    *destination*. Both *origin, destination* params accept either Port
    Codes or Region slugs, making it possible to query for average prices
    per day between geographic groups of ports.
    """
    ## All parameters are required and must not be empty
    parameters = ['date_from', 'date_to', 'origin', 'destination']
    for param in parameters:
        if param not in request.query or not request.query[param]:
            return Error('Missing parameters...',
                         received=list(request.query.keys()))
    ## Convert date strings to the python datetime
    try:
        params = parse_dates(request.query)
    except Exception as err:
        return Error('Incorrect date(s)...',
                     received=list(request.query[k] for k in ['date_from', 'date_to']))
    ## Normalize origin and destination keys
    params = parse_orig_dest_get(params)
    ## Choose correct query based on the origin and destination string length
    query = get_query(params)
    ## Fetch average prices from the DB
    with closing(DBSession()) as db:
        result = db(query, params)
        return(json.dumps(to_dict(result), **pretty_json))


@route(['/put'], method=['POST'])
def rates_put():
    """
    Implement an API endpoint where you can upload a price, including
    the following parameters: *date_from, date_to, origin_code,
    destination_code, price*.
    """
    ## All parameters except date_to are required and must not be empty
    parameters = ['origin_code', 'destination_code', 'date_from', 'price']
    for param in parameters:
        if param not in request.forms or not request.forms[param]:
            return Error('Missing parameters...',
                         received=list(request.forms.keys()))
    ## Convert date string to the python datetime
    try:
        params = parse_dates(request.forms)
    except Exception as err:
        return Error('Incorrect date(s)...',
                     received=list(request.forms[k] for k in ['date_from', 'date_to']))
    ## Normalize origin_code and destination_code keys
    try:
        params = parse_orig_dest_post(params)
    except Exception as err:
        return Error('Incorrect port code...',
                     received=list(request.forms[k] for k in ['origin_code', 'destination_code']))
     ## Normalize price
    try:
        params = parse_price(params)
    except Exception as err:
        return Error('Price must be an integer...',
                     received=request['price'])
    ## Query to insert data into the DB
    query = 'INSERT INTO prices (orig_code, dest_code, day, price) VALUES %s '
    template = '(%(origin_code)s, %(destination_code)s, %(date_from)s, %(price)s)'
    ## Connect to the DB and insert data
    with closing(DBSession()) as db:
        try:
            param_list = post_param_list(params)
            db.execute_values(query, param_list, template)
            db.connection.commit()
        except Exception as err:
            print(err)
            return Error('Server Error :(', code=500)
        else:
            return json.dumps({'success': True}, **pretty_json)



if __name__ == "__main__":
    HOST = '0.0.0.0'
    PORT = 8888
    DEBUG = False
    QUIET = False
    run(host=HOST, port=PORT, server='waitress', debug=DEBUG, quiet=QUIET)
