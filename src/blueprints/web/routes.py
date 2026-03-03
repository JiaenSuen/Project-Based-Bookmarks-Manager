from flask import render_template, redirect, url_for, request, flash
from src.extensions import db
from src.models.project import Project
from src.models.bookmark import Bookmark
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, URLField
from wtforms.validators import DataRequired, Length, URL
from flask import Blueprint
from . import web_bp

 

class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description')
    submit = SubmitField('New Project')

class BookmarkForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    url = URLField('Link', validators=[DataRequired(), URL()])
    description = TextAreaField('Description')
    submit = SubmitField('Save Bookmarks')

 

@web_bp.route('/', methods=['GET', 'POST'])  
def project_list():
    form = ProjectForm()
    
    if form.validate_on_submit():          
        project = Project(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Projects have been added.', 'success')
        return redirect(url_for('web.project_list'))  
    
    projects = Project.query.order_by(Project.created_at.desc()).all()
    return render_template('project_list.html', projects=projects, form=form)
@web_bp.route('/project/new', methods=['POST'])
def project_create():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(project)
        db.session.commit()
        flash('Projects have been added.', 'success')
        return redirect(url_for('web.project_list'))
    flash('Form validation failed', 'danger')
    return redirect(url_for('web.project_list'))
@web_bp.route('/project/<int:project_id>/delete', methods=['POST'])
def project_delete(project_id):
    project = Project.query.get_or_404(project_id)

    db.session.delete(project)
    db.session.commit()

    flash('Project deleted', 'success')
    return redirect(url_for('web.project_list'))





@web_bp.route('/project/<int:project_id>')
def project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    form = BookmarkForm()
    return render_template('project_detail.html', project=project, form=form)

@web_bp.route('/project/<int:project_id>/bookmark/new', methods=['POST'])
def bookmark_create(project_id):
    project = Project.query.get_or_404(project_id)
    form = BookmarkForm()
    if form.validate_on_submit():
        bookmark = Bookmark(
            project_id=project.id,
            title=form.title.data,
            url=form.url.data,
            description=form.description.data
        )
        db.session.add(bookmark)
        db.session.commit()
        flash('Bookmarks have been added', 'success')
        return redirect(url_for('web.project_detail', project_id=project.id))
    flash('Form validation failed', 'danger')
    return redirect(url_for('web.project_detail', project_id=project.id))

@web_bp.route('/bookmark/<int:bookmark_id>/delete', methods=['POST'])
def bookmark_delete(bookmark_id):
    bookmark = Bookmark.query.get_or_404(bookmark_id)
    project_id = bookmark.project_id
    db.session.delete(bookmark)
    db.session.commit()
    flash('Bookmarks have been deleted', 'success')
    return redirect(url_for('web.project_detail', project_id=project_id))