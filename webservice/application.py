from flask import Flask
from webservice.admin.job import module as job_admin
from webservice.index.article import module as article_index
from webservice.index.stat import module as stat_index
from webservice.view.admin import module as admin_view
from webservice.view.index import module as index_view


app = Flask(__name__)
app.register_blueprint(job_admin, url_prefix="/admin")
app.register_blueprint(article_index, url_prefix="/article")
app.register_blueprint(admin_view, url_prefix="/admin")
app.register_blueprint(index_view, url_prefix="/")
app.register_blueprint(stat_index, url_prefix="/stat")


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
