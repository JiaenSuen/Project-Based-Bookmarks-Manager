from flask import render_template, redirect, url_for, request, flash
from src.extensions import db
from src.models.project import Project
from src.models.bookmark import Bookmark
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField, HiddenField
from wtforms.validators import DataRequired, Length, URL, Optional
from flask import Blueprint
from . import web_bp


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('Create Project')


class BookmarkForm(FlaskForm):
    id = HiddenField()  # Used when editing
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=200)],
        render_kw={"placeholder": "e.g. API Documentation"}
    )
    url = URLField(
        "URL",
        validators=[DataRequired(), URL(message="Please enter a valid URL")],
        render_kw={"placeholder": "https://..."}
    )
    description = TextAreaField(
        "Description",
        validators=[Optional(), Length(max=1000)],
        render_kw={"rows": 3, "placeholder": "Optional notes..."}
    )
    submit = SubmitField("Save")


@web_bp.route('/', methods=['GET', 'POST'])
def project_list():
    form = ProjectForm()

    if form.validate_on_submit():
        project = Project(
            name=form.name.data.strip(),
            description=form.description.data.strip() or None
        )
        db.session.add(project)
        db.session.commit()
        flash('Project created successfully.', 'success')
        return redirect(url_for('web.project_list'))

    projects = Project.query.order_by(Project.created_at.desc()).all()
    edit_form = ProjectForm()  # 用來產生 csrf_token，如果 modal 需要

    return render_template(
        'project_list.html',
        projects=projects,
        form=form,
        edit_form=edit_form
    )


@web_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    create_form = BookmarkForm()
    return render_template(
        "project_detail.html",
        project=project,
        create_form=create_form,
    )


@web_bp.route('/project/<int:project_id>/delete', methods=['POST'])
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)
    # 如果模型沒有設定 cascade，可以手動刪除關聯書籤
    # Bookmark.query.filter_by(project_id=project.id).delete()
    db.session.delete(project)
    db.session.commit()
    flash('Project and its bookmarks have been deleted.', 'success')
    return redirect(url_for('web.project_list'))


@web_bp.route('/project/<int:project_id>/update', methods=['POST'])
def project_update(project_id):
    project = Project.query.get_or_404(project_id)

    name = request.form.get('name', '').strip()
    description = request.form.get('description', '').strip()

    if not name:
        flash('Project name is required.', 'danger')
        return redirect(url_for('web.project_list'))

    project.name = name
    project.description = description or None
    db.session.commit()

    flash('Project updated successfully.', 'success')
    return redirect(url_for('web.project_list'))


@web_bp.route("/project/<int:project_id>/bookmark/new", methods=["POST"])
def bookmark_create(project_id):
    project = Project.query.get_or_404(project_id)
    form = BookmarkForm()

    if form.validate_on_submit():
        bookmark = Bookmark(
            project_id=project.id,
            title=form.title.data.strip(),
            url=form.url.data.strip(),
            description=form.description.data.strip() or None,
        )
        db.session.add(bookmark)
        db.session.commit()
        flash("Bookmark created successfully.", "success")
    else:
        flash("Form validation failed. Please check your input.", "danger")

    return redirect(url_for("web.project_detail", project_id=project.id))


@web_bp.route("/bookmark/<int:bookmark_id>/edit", methods=["GET", "POST"])
def bookmark_edit(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    project = bookmark.project

    form = BookmarkForm(obj=bookmark)

    if form.validate_on_submit():
        form.populate_obj(bookmark)
        db.session.commit()
        flash("Bookmark updated successfully.", "success")
        return redirect(url_for("web.project_detail", project_id=project.id))

    return render_template(
        "project_detail.html",
        project=project,
        create_form=BookmarkForm(),
        edit_form=form,
        editing_bookmark=bookmark,
    )


@web_bp.route("/bookmark/<int:bookmark_id>/delete", methods=["POST"])
def bookmark_delete(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    project_id = bookmark.project_id
    db.session.delete(bookmark)
    db.session.commit()
    flash("Bookmark deleted.", "success")
    return redirect(url_for("web.project_detail", project_id=project_id))