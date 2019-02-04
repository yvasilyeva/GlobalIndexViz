import os
basedir = os.path.abspath(os.path.dirname(__file__))
DB_URL="sqlite:///" + os.path.join(basedir, '', 'gl_index_data.db')