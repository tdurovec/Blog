from flask import Blueprint, render_template
from flask import session, request, redirect, url_for

from models import db, Articles
from forms import ArticleForm
from utils import login_required

from task import notify_newsletter

article = Blueprint("article", __name__)

@article.route("/")
def view_home():
    return render_template("Base/home_page.html")

@article.route("/about/")
def view_about():
    return render_template("Base/about.html")

@article.route("/articles/")
def view_articles():
    page = request.args.get("page", 1, type=int)
    paginate = Articles.query.order_by(Articles.id.desc()).paginate(page, 5, False)
    return render_template("Article/articles.html", articles=paginate.items, paginate=paginate)

@article.route("/article/<int:art_id>")
def view_article(art_id):
    article = Articles.query.filter_by(id=art_id).first()
    if article:
        return render_template("Article/article.html", article=article)
    return render_template("Article/article_not_found.html", art_id=art_id)

@article.route("/article/<int:art_id>/edit", methods=["GET"])
def view_edit_article(art_id):
    article = Articles.query.filter_by(id=art_id).first()
    if article:
        form = ArticleForm()
        form.title.data = article.title
        form.content.data = article.content
        return render_template("Article/article_editor.html", form=form, article=article)
    return render_template("Article/article_not_found.html", article=art_id)

@article.route("/article/<int:art_id>/edit", methods=["POST"])
def edit_article(art_id):
    print(art_id)
    
    article = Articles.query.filter_by(id=art_id).first()

    if article:
        edit_form = ArticleForm()
        if edit_form.validate():
            article.title = edit_form.title.data
            article.content = edit_form.content.data
            article.html_render = edit_form.html_render.data
            db.session.add(article)
            db.session.commit()
            return redirect(url_for("article.view_article", art_id=art_id))
        else:
            print("Error")
            return redirect(url_for("article.view_article", art_id=art_id))

@article.route("/article/<int:art_id>/delete")
def delete_article(art_id):

    Articles.query.filter_by(id=art_id).delete()
    db.session.commit()

    return redirect(url_for("article.view_articles")) 

@article.route("/add-article/", methods=["GET"])
def view_add_article():
    article_form = ArticleForm()
    return render_template("Article/article_editor.html", form=article_form)

@article.route("/add-article/", methods=["POST"])
@login_required
def add_article():
    add_form = ArticleForm(request.form)
    if add_form.validate():
        new_article = Articles(
            title = add_form.title.data,
            content = add_form.content.data,
            html_render = add_form.html_render.data,
            author = session["logged"]
            )
        db.session.add(new_article)
        db.session.commit()

        article_url = url_for("article.view_article", art_id=new_article.id)
        article_url = request.url_root + article_url[1:]
        notify_newsletter.delay(article_url)

        return redirect(url_for("article.view_articles"))
    else:
        return render_template("Article/article_editor.html", form=add_form)